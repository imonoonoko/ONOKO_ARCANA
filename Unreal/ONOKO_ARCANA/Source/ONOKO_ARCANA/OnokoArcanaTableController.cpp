#include "OnokoArcanaTableController.h"

#include "OnokoArcanaCardActor.h"
#include "OnokoArcanaOneCardSession.h"
#include "OnokoArcanaOneCardViewModel.h"
#include "OnokoArcanaReadingHistoryViewModel.h"
#include "OnokoArcanaReadingSaveGame.h"
#include "OnokoArcanaReadingSaveLibrary.h"
#include "OnokoArcanaSpreadReadingSession.h"
#include "OnokoArcanaSpreadReadingViewModel.h"
#include "Components/TextRenderComponent.h"
#include "Engine/TextRenderActor.h"
#include "Engine/World.h"

AOnokoArcanaTableController::AOnokoArcanaTableController()
{
	PrimaryActorTick.bCanEverTick = false;
}

void AOnokoArcanaTableController::BeginPlay()
{
	Super::BeginPlay();
	InitializeTable();
}

bool AOnokoArcanaTableController::InitializeTable()
{
	if (!InitializeSpreadRegistry())
	{
		OnTableStateChanged();
		return false;
	}

	UOnokoArcanaOneCardViewModel* ActiveViewModel = EnsureViewModel();
	if (!ActiveViewModel)
	{
		LastErrorMessage = TEXT("Could not create one-card view model.");
		return false;
	}

	const bool bInitialized = ActiveViewModel->Initialize();
	CaptureLastError();

	if (bInitialized && ReadingCardActor && ActiveViewModel->Session && ActiveViewModel->Session->Deck)
	{
		ReadingCardActor->SetBackTexture(ActiveViewModel->Session->Deck->BackTexture);
		ReadingCardActor->ShowBack();
	}

	OnTableStateChanged();
	return bInitialized;
}

bool AOnokoArcanaTableController::InitializeSpreadRegistry()
{
	UOnokoArcanaSpreadRegistry* ActiveRegistry = EnsureSpreadRegistry();
	if (!ActiveRegistry)
	{
		LastErrorMessage = TEXT("Could not create spread registry.");
		return false;
	}

	FOnokoArcanaSpreadDefinition ResolvedSpread;
	if (!ActiveRegistry->FindSpreadById(ActiveSpreadId, ResolvedSpread))
	{
		ActiveSpreadId = ActiveRegistry->GetDefaultSpreadId();
		if (!ActiveRegistry->FindSpreadById(ActiveSpreadId, ResolvedSpread))
		{
			LastErrorMessage = TEXT("Could not resolve the default spread definition.");
			return false;
		}
	}

	ActiveSpreadDefinition = ResolvedSpread;
	LastErrorMessage.Reset();
	return true;
}

bool AOnokoArcanaTableController::SelectSpread(FName SpreadId)
{
	if (SpreadId.IsNone())
	{
		LastErrorMessage = TEXT("Spread id is required.");
		OnTableStateChanged();
		return false;
	}

	if (HasCurrentDraw() && SpreadId != ActiveSpreadId)
	{
		LastErrorMessage = TEXT("Reset the current reading before changing spreads.");
		OnTableStateChanged();
		return false;
	}

	UOnokoArcanaSpreadRegistry* ActiveRegistry = EnsureSpreadRegistry();
	if (!ActiveRegistry)
	{
		LastErrorMessage = TEXT("Could not create spread registry.");
		OnTableStateChanged();
		return false;
	}

	FOnokoArcanaSpreadDefinition ResolvedSpread;
	if (!ActiveRegistry->FindSpreadById(SpreadId, ResolvedSpread))
	{
		LastErrorMessage = FString::Printf(TEXT("Unknown spread id: %s"), *SpreadId.ToString());
		OnTableStateChanged();
		return false;
	}

	ActiveSpreadId = SpreadId;
	ActiveSpreadDefinition = ResolvedSpread;
	LastErrorMessage.Reset();
	OnTableStateChanged();
	return true;
}

bool AOnokoArcanaTableController::SelectSpreadSlot(FName PositionKey)
{
	if (IsOneCardSpread())
	{
		LastErrorMessage = TEXT("Spread slot selection is available only for multi-card spreads.");
		OnTableStateChanged();
		return false;
	}

	UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel();
	if (!ActiveSpreadViewModel || !ActiveSpreadViewModel->Session || !ActiveSpreadViewModel->Session->bHasActiveReading)
	{
		LastErrorMessage = TEXT("Start a spread reading before selecting a spread slot.");
		OnTableStateChanged();
		return false;
	}

	const bool bSelected = ActiveSpreadViewModel->SelectSlot(PositionKey);
	CaptureLastSpreadError();
	if (bSelected)
	{
		SyncSpreadCardActors();
	}
	OnTableStateChanged();
	return bSelected;
}

TArray<FOnokoArcanaSpreadDefinition> AOnokoArcanaTableController::GetAvailableSpreads() const
{
	return SpreadRegistry ? SpreadRegistry->Spreads : TArray<FOnokoArcanaSpreadDefinition>();
}

FOnokoArcanaSpreadDefinition AOnokoArcanaTableController::GetActiveSpread() const
{
	return ActiveSpreadDefinition;
}

FString AOnokoArcanaTableController::GetActiveSpreadDisplayText() const
{
	if (ActiveSpreadDefinition.SpreadId.IsNone())
	{
		return TEXT("スプレッド未設定");
	}

	return FString::Printf(
		TEXT("%s (%d枚)"),
		*ActiveSpreadDefinition.DisplayName,
		ActiveSpreadDefinition.Slots.Num());
}

FString AOnokoArcanaTableController::GetActiveSpreadSlotListText() const
{
	return SpreadRegistry ? SpreadRegistry->GetSpreadSlotListText(ActiveSpreadId) : FString();
}

FString AOnokoArcanaTableController::GetAvailableSpreadListText() const
{
	return SpreadRegistry ? SpreadRegistry->GetSpreadListText() : FString();
}

FString AOnokoArcanaTableController::GetSelectedSpreadSlotText() const
{
	if (IsOneCardSpread() || !SpreadViewModel || !SpreadViewModel->Session)
	{
		return FString();
	}

	FOnokoArcanaReadingCardState State;
	if (!SpreadViewModel->Session->GetSelectedCardState(State))
	{
		return TEXT("選択位置: 未選択");
	}

	return FString::Printf(TEXT("選択位置: %s [%s]"), *State.PositionLabel, *State.PositionKey.ToString());
}

bool AOnokoArcanaTableController::StartReading(const FString& Question)
{
	if (!InitializeSpreadRegistry())
	{
		OnTableStateChanged();
		return false;
	}

	const FString EffectiveQuestion = Question.IsEmpty() ? DefaultQuestion : Question;
	if (!IsOneCardSpread())
	{
		UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel();
		if (!ActiveSpreadViewModel)
		{
			LastErrorMessage = TEXT("Could not create spread reading view model.");
			OnTableStateChanged();
			return false;
		}

		if (!ActiveSpreadViewModel->Session && !ActiveSpreadViewModel->Initialize())
		{
			CaptureLastSpreadError();
			OnTableStateChanged();
			return false;
		}

		const bool bStarted = ActiveSpreadViewModel->StartReading(
			EffectiveQuestion,
			ActiveSpreadDefinition,
			DeterministicSeed,
			bUseDeterministicSeed);
		CaptureLastSpreadError();
		if (bStarted)
		{
			EnsureSpreadCardActors(ActiveSpreadDefinition.Slots.Num());
			SyncSpreadCardActors();
		}
		OnTableStateChanged();
		return bStarted;
	}

	UOnokoArcanaOneCardViewModel* ActiveViewModel = EnsureViewModel();
	if (!ActiveViewModel)
	{
		LastErrorMessage = TEXT("Could not create one-card view model.");
		return false;
	}

	const bool bStarted = ActiveViewModel->StartReading(EffectiveQuestion, DeterministicSeed, bUseDeterministicSeed);
	CaptureLastError();

	if (bStarted && ReadingCardActor && ActiveViewModel->Session && ActiveViewModel->Session->Deck)
	{
		ReadingCardActor->SetBackTexture(ActiveViewModel->Session->Deck->BackTexture);
		ReadingCardActor->ShowBack();
	}

	OnTableStateChanged();
	return bStarted;
}

bool AOnokoArcanaTableController::DrawCard(bool bRevealImmediately)
{
	if (!InitializeSpreadRegistry())
	{
		OnTableStateChanged();
		return false;
	}

	if (!IsOneCardSpread())
	{
		UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel();
		if (!ActiveSpreadViewModel)
		{
			LastErrorMessage = TEXT("Could not create spread reading view model.");
			OnTableStateChanged();
			return false;
		}

		if (!ActiveSpreadViewModel->Session || !ActiveSpreadViewModel->Session->bHasActiveReading)
		{
			if (!StartReading(DefaultQuestion))
			{
				return false;
			}
		}

		if (ActiveSpreadViewModel->HasDrawnSpread())
		{
			LastErrorMessage = TEXT("Reset the current spread before drawing again.");
			OnTableStateChanged();
			return false;
		}

		const bool bDrawn = ActiveSpreadViewModel->DrawSpread(bAllowReversed);
		CaptureLastSpreadError();
		if (!bDrawn)
		{
			OnTableStateChanged();
			return false;
		}

		if (bRevealImmediately)
		{
			while (ActiveSpreadViewModel->CanRevealNext())
			{
				if (!ActiveSpreadViewModel->RevealNext())
				{
					break;
				}
			}
			CaptureLastSpreadError();
		}

		const bool bSynced = SyncSpreadCardActors();
		OnTableStateChanged();
		return bSynced;
	}

	UOnokoArcanaOneCardViewModel* ActiveViewModel = EnsureViewModel();
	if (!ActiveViewModel)
	{
		LastErrorMessage = TEXT("Could not create one-card view model.");
		return false;
	}

	if (!ActiveViewModel->HasCurrentDraw() && !ActiveViewModel->CanDraw())
	{
		if (!StartReading(DefaultQuestion))
		{
			return false;
		}
	}

	const bool bDrawn = ActiveViewModel->DrawOne(bAllowReversed);
	CaptureLastError();

	if (!bDrawn)
	{
		OnTableStateChanged();
		return false;
	}

	const bool bSynced = SyncCardActorToViewModel(bRevealImmediately);
	OnCardDrawn(ActiveViewModel->GetCurrentDraw());
	OnTableStateChanged();
	return bSynced;
}

bool AOnokoArcanaTableController::RevealCard()
{
	if (!IsOneCardSpread())
	{
		UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel();
		if (!ActiveSpreadViewModel)
		{
			LastErrorMessage = TEXT("Could not create spread reading view model.");
			OnTableStateChanged();
			return false;
		}

		const bool bRevealed = ActiveSpreadViewModel->RevealNext();
		CaptureLastSpreadError();
		if (bRevealed)
		{
			SyncSpreadCardActors();
		}
		OnTableStateChanged();
		return bRevealed;
	}

	if (!ReadingCardActor)
	{
		LastErrorMessage = TEXT("ReadingCardActor is not assigned.");
		return false;
	}

	const bool bRevealed = ReadingCardActor->RevealFront();
	OnTableStateChanged();
	return bRevealed;
}

void AOnokoArcanaTableController::SubmitUserInterpretation(const FString& Text)
{
	if (!IsOneCardSpread())
	{
		if (UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel())
		{
			ActiveSpreadViewModel->SubmitSelectedSlotInterpretation(Text);
			CaptureLastSpreadError();
		}
		OnTableStateChanged();
		return;
	}

	if (UOnokoArcanaOneCardViewModel* ActiveViewModel = EnsureViewModel())
	{
		ActiveViewModel->SubmitUserInterpretation(Text);
		CaptureLastError();
	}
	OnTableStateChanged();
}

bool AOnokoArcanaTableController::RevealGuide()
{
	if (!IsOneCardSpread())
	{
		UOnokoArcanaSpreadReadingViewModel* ActiveSpreadViewModel = EnsureSpreadViewModel();
		if (!ActiveSpreadViewModel)
		{
			LastErrorMessage = TEXT("Could not create spread reading view model.");
			OnTableStateChanged();
			return false;
		}

		const bool bRevealed = ActiveSpreadViewModel->RevealSelectedGuide();
		CaptureLastSpreadError();
		OnTableStateChanged();
		return bRevealed;
	}

	UOnokoArcanaOneCardViewModel* ActiveViewModel = EnsureViewModel();
	if (!ActiveViewModel)
	{
		LastErrorMessage = TEXT("Could not create one-card view model.");
		return false;
	}

	const bool bRevealed = ActiveViewModel->RevealGuide();
	CaptureLastError();
	OnTableStateChanged();
	return bRevealed;
}

void AOnokoArcanaTableController::ResetTable()
{
	if (SpreadViewModel)
	{
		SpreadViewModel->ResetReading();
		CaptureLastSpreadError();
	}

	if (ViewModel)
	{
		ViewModel->ResetReading();
		CaptureLastError();
	}

	if (ReadingCardActor)
	{
		ReadingCardActor->ShowBack();
	}
	for (AOnokoArcanaCardActor* CardActor : SpreadCardActors)
	{
		if (CardActor)
		{
			CardActor->ShowBack();
			CardActor->SetActorHiddenInGame(false);
		}
	}

	OnTableStateChanged();
}

bool AOnokoArcanaTableController::SaveCurrentReading()
{
	if (!IsOneCardSpread())
	{
		if (!SpreadViewModel || !SpreadViewModel->Session)
		{
			LastErrorMessage = TEXT("There is no active spread reading session to save.");
			OnTableStateChanged();
			return false;
		}

		FOnokoArcanaSavedReading Reading;
		if (!UOnokoArcanaReadingSaveLibrary::MakeSavedReadingFromSpreadSession(SpreadViewModel->Session, Reading, LastErrorMessage))
		{
			OnTableStateChanged();
			return false;
		}

		const bool bSaved = UOnokoArcanaReadingSaveLibrary::SaveReadingToSlot(
			Reading,
			SaveSlotName,
			SaveUserIndex,
			LastErrorMessage);
		if (bSaved)
		{
			RefreshReadingHistory();
		}
		OnTableStateChanged();
		return bSaved;
	}

	if (!ViewModel || !ViewModel->Session)
	{
		LastErrorMessage = TEXT("There is no active reading session to save.");
		OnTableStateChanged();
		return false;
	}

	FOnokoArcanaSavedReading Reading;
	if (!UOnokoArcanaReadingSaveLibrary::MakeSavedReadingFromSession(ViewModel->Session, Reading, LastErrorMessage))
	{
		OnTableStateChanged();
		return false;
	}

	Reading.SpreadId = ActiveSpreadId.ToString();
	Reading.SpreadDisplayName = ActiveSpreadDefinition.DisplayName;
	Reading.CardCount = 1;
	if (ActiveSpreadDefinition.Slots.Num() > 0)
	{
		const FOnokoArcanaSpreadSlotDefinition& Slot = ActiveSpreadDefinition.Slots[0];
		Reading.PositionKey = Slot.PositionKey.ToString();
		Reading.PositionLabel = Slot.DisplayLabel;
	}

	const bool bSaved = UOnokoArcanaReadingSaveLibrary::SaveReadingToSlot(
		Reading,
		SaveSlotName,
		SaveUserIndex,
		LastErrorMessage);
	if (bSaved)
	{
		RefreshReadingHistory();
	}
	OnTableStateChanged();
	return bSaved;
}

bool AOnokoArcanaTableController::LoadReadingHistory(UOnokoArcanaReadingSaveGame*& OutSaveGame)
{
	const bool bLoaded = UOnokoArcanaReadingSaveLibrary::LoadReadingsFromSlot(
		SaveSlotName,
		SaveUserIndex,
		OutSaveGame,
		LastErrorMessage);
	OnTableStateChanged();
	return bLoaded;
}

bool AOnokoArcanaTableController::RefreshReadingHistory()
{
	UOnokoArcanaReadingHistoryViewModel* ActiveHistoryViewModel = EnsureHistoryViewModel();
	if (!ActiveHistoryViewModel)
	{
		LastErrorMessage = TEXT("Could not create reading history view model.");
		OnTableStateChanged();
		return false;
	}

	const bool bLoaded = ActiveHistoryViewModel->LoadFromSlot(SaveSlotName, SaveUserIndex);
	LastErrorMessage = ActiveHistoryViewModel->LastErrorMessage;
	OnTableStateChanged();
	return bLoaded;
}

bool AOnokoArcanaTableController::SelectHistoryReading(int32 Index)
{
	UOnokoArcanaReadingHistoryViewModel* ActiveHistoryViewModel = EnsureHistoryViewModel();
	if (!ActiveHistoryViewModel)
	{
		LastErrorMessage = TEXT("Could not create reading history view model.");
		OnTableStateChanged();
		return false;
	}

	const bool bSelected = ActiveHistoryViewModel->SelectReading(Index);
	LastErrorMessage = ActiveHistoryViewModel->LastErrorMessage;
	OnTableStateChanged();
	return bSelected;
}

FOnokoArcanaDrawResult AOnokoArcanaTableController::GetCurrentDraw() const
{
	if (!IsOneCardSpread() && SpreadViewModel && SpreadViewModel->Session)
	{
		FOnokoArcanaReadingCardState SelectedState;
		if (SpreadViewModel->Session->GetSelectedCardState(SelectedState) && SelectedState.bHasDraw)
		{
			return SelectedState.Draw;
		}
	}
	return ViewModel ? ViewModel->GetCurrentDraw() : FOnokoArcanaDrawResult();
}

bool AOnokoArcanaTableController::HasCurrentDraw() const
{
	if (!IsOneCardSpread())
	{
		return SpreadViewModel && SpreadViewModel->HasDrawnSpread();
	}
	return ViewModel && ViewModel->HasCurrentDraw();
}

bool AOnokoArcanaTableController::IsOneCardSpread() const
{
	return ActiveSpreadId == FName(TEXT("one_card"));
}

bool AOnokoArcanaTableController::IsSpreadReadingActive() const
{
	return SpreadViewModel && SpreadViewModel->Session && SpreadViewModel->Session->bHasActiveReading;
}

UOnokoArcanaSpreadRegistry* AOnokoArcanaTableController::EnsureSpreadRegistry()
{
	if (!SpreadRegistry)
	{
		SpreadRegistry = NewObject<UOnokoArcanaSpreadRegistry>(this);
	}

	if (SpreadRegistry && SpreadRegistry->GetSpreadCount() == 0)
	{
		SpreadRegistry->InitializeBuiltInSpreads();
	}

	return SpreadRegistry;
}

UOnokoArcanaOneCardViewModel* AOnokoArcanaTableController::EnsureViewModel()
{
	if (!ViewModel)
	{
		ViewModel = NewObject<UOnokoArcanaOneCardViewModel>(this);
	}
	return ViewModel;
}

UOnokoArcanaSpreadReadingViewModel* AOnokoArcanaTableController::EnsureSpreadViewModel()
{
	if (!SpreadViewModel)
	{
		SpreadViewModel = NewObject<UOnokoArcanaSpreadReadingViewModel>(this);
	}
	return SpreadViewModel;
}

UOnokoArcanaReadingHistoryViewModel* AOnokoArcanaTableController::EnsureHistoryViewModel()
{
	if (!HistoryViewModel)
	{
		HistoryViewModel = NewObject<UOnokoArcanaReadingHistoryViewModel>(this);
	}
	return HistoryViewModel;
}

bool AOnokoArcanaTableController::SyncCardActorToViewModel(bool bRevealImmediately)
{
	if (!ReadingCardActor)
	{
		LastErrorMessage = TEXT("ReadingCardActor is not assigned.");
		return false;
	}

	if (!ViewModel || !ViewModel->HasCurrentDraw())
	{
		LastErrorMessage = TEXT("There is no current draw to show.");
		return false;
	}

	const FOnokoArcanaDrawResult Draw = ViewModel->GetCurrentDraw();
	const bool bCardSet = ReadingCardActor->SetCard(Draw.Card, Draw.Orientation, bRevealImmediately);
	if (!bCardSet)
	{
		LastErrorMessage = TEXT("Could not apply drawn card texture to the reading card actor.");
	}
	return bCardSet;
}

bool AOnokoArcanaTableController::EnsureSpreadCardActors(int32 RequiredCount)
{
	if (RequiredCount <= 0)
	{
		HideUnusedSpreadCardActors(0);
		HideUnusedSpreadSlotLabels(0);
		return true;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		LastErrorMessage = TEXT("World is not available for spread card actor placement.");
		return false;
	}

	if (ReadingCardActor && SpreadCardActors.Num() == 0)
	{
		SpreadCardActors.Add(ReadingCardActor);
	}

	while (SpreadCardActors.Num() < RequiredCount)
	{
		FActorSpawnParameters SpawnParams;
		AOnokoArcanaCardActor* CardActor = World->SpawnActor<AOnokoArcanaCardActor>(
			AOnokoArcanaCardActor::StaticClass(),
			FVector::ZeroVector,
			FRotator(0.0f, 90.0f, 0.0f),
			SpawnParams);
		if (!CardActor)
		{
			LastErrorMessage = TEXT("Could not spawn a spread card actor.");
			return false;
		}

		CardActor->ConfigureCardScale(72.0f, 108.0f);
		SpreadCardActors.Add(CardActor);
	}

	PlaceSpreadCardActors();
	SyncSpreadSlotLabels();
	HideUnusedSpreadCardActors(RequiredCount);
	LastErrorMessage.Reset();
	return true;
}

bool AOnokoArcanaTableController::SyncSpreadCardActors()
{
	if (!SpreadViewModel || !SpreadViewModel->Session)
	{
		LastErrorMessage = TEXT("There is no active spread reading to show.");
		return false;
	}

	const TArray<FOnokoArcanaReadingCardState>& CardStates = SpreadViewModel->Session->CardStates;
	if (!EnsureSpreadCardActors(CardStates.Num()))
	{
		return false;
	}

	TSoftObjectPtr<UTexture2D> BackTexture;
	if (SpreadViewModel->Session->Deck)
	{
		BackTexture = SpreadViewModel->Session->Deck->BackTexture;
	}

	bool bAllSynced = true;
	for (int32 Index = 0; Index < CardStates.Num(); ++Index)
	{
		AOnokoArcanaCardActor* CardActor = SpreadCardActors.IsValidIndex(Index) ? SpreadCardActors[Index] : nullptr;
		if (!CardActor)
		{
			bAllSynced = false;
			continue;
		}

		const FOnokoArcanaReadingCardState& State = CardStates[Index];
		CardActor->SetActorHiddenInGame(false);
		CardActor->ConfigureCardScale(State.bSelected ? 78.0f : 72.0f, State.bSelected ? 117.0f : 108.0f);
		if (!BackTexture.IsNull())
		{
			CardActor->SetBackTexture(BackTexture);
		}

		if (State.bHasDraw && State.Draw.bSuccess)
		{
			bAllSynced &= CardActor->SetCard(State.Draw.Card, State.Draw.Orientation, State.bRevealed);
		}
		else
		{
			bAllSynced &= CardActor->ShowBack();
		}
	}

	HideUnusedSpreadCardActors(CardStates.Num());
	SyncSpreadSlotLabels();
	if (!bAllSynced)
	{
		LastErrorMessage = TEXT("One or more spread cards could not apply their texture.");
	}
	return bAllSynced;
}

bool AOnokoArcanaTableController::EnsureSpreadSlotLabels(int32 RequiredCount)
{
	if (RequiredCount <= 0)
	{
		HideUnusedSpreadSlotLabels(0);
		return true;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		LastErrorMessage = TEXT("World is not available for spread slot labels.");
		return false;
	}

	while (SpreadSlotLabelActors.Num() < RequiredCount)
	{
		FActorSpawnParameters SpawnParams;
		ATextRenderActor* LabelActor = World->SpawnActor<ATextRenderActor>(
			ATextRenderActor::StaticClass(),
			FVector::ZeroVector,
			FRotator(90.0f, 0.0f, 180.0f),
			SpawnParams);
		if (!LabelActor)
		{
			LastErrorMessage = TEXT("Could not spawn a spread slot label.");
			return false;
		}

		if (UTextRenderComponent* TextComponent = LabelActor->GetTextRender())
		{
			TextComponent->SetHorizontalAlignment(EHTA_Center);
			TextComponent->SetVerticalAlignment(EVRTA_TextCenter);
			TextComponent->SetWorldSize(17.0f);
			TextComponent->SetTextRenderColor(FColor(214, 236, 255, 255));
			TextComponent->SetText(FText::GetEmpty());
		}
		LabelActor->SetActorHiddenInGame(false);
		SpreadSlotLabelActors.Add(LabelActor);
	}

	HideUnusedSpreadSlotLabels(RequiredCount);
	return true;
}

void AOnokoArcanaTableController::PlaceSpreadCardActors()
{
	const int32 Count = SpreadViewModel && SpreadViewModel->Session
		? SpreadViewModel->Session->CardStates.Num()
		: ActiveSpreadDefinition.Slots.Num();
	if (Count <= 0)
	{
		return;
	}

	const float StartOffset = -0.5f * SpreadCardSpacingCentimeters * static_cast<float>(Count - 1);
	for (int32 Index = 0; Index < Count; ++Index)
	{
		AOnokoArcanaCardActor* CardActor = SpreadCardActors.IsValidIndex(Index) ? SpreadCardActors[Index] : nullptr;
		if (!CardActor)
		{
			continue;
		}

		const FVector Location(
			0.0f,
			SpreadCardCenterYOffsetCentimeters + StartOffset + SpreadCardSpacingCentimeters * static_cast<float>(Index),
			8.0f);
		CardActor->SetActorLocation(Location);
		CardActor->SetActorRotation(FRotator(0.0f, 90.0f, 0.0f));
		CardActor->SetActorHiddenInGame(false);
	}
	SyncSpreadSlotLabels();
}

void AOnokoArcanaTableController::SyncSpreadSlotLabels()
{
	const int32 Count = SpreadViewModel && SpreadViewModel->Session
		? SpreadViewModel->Session->CardStates.Num()
		: ActiveSpreadDefinition.Slots.Num();
	if (Count <= 0 || !EnsureSpreadSlotLabels(Count))
	{
		return;
	}

	const float StartOffset = -0.5f * SpreadCardSpacingCentimeters * static_cast<float>(Count - 1);
	for (int32 Index = 0; Index < Count; ++Index)
	{
		ATextRenderActor* LabelActor = SpreadSlotLabelActors.IsValidIndex(Index) ? SpreadSlotLabelActors[Index] : nullptr;
		if (!LabelActor)
		{
			continue;
		}

		const FVector Location(
			SpreadLabelXOffsetCentimeters,
			SpreadCardCenterYOffsetCentimeters + StartOffset + SpreadCardSpacingCentimeters * static_cast<float>(Index),
			14.0f);
		LabelActor->SetActorLocation(Location);
		LabelActor->SetActorRotation(FRotator(90.0f, 0.0f, 180.0f));
		LabelActor->SetActorHiddenInGame(false);

		FString PositionLabel;
		FString PositionKey;
		bool bSelected = false;
		if (SpreadViewModel && SpreadViewModel->Session && SpreadViewModel->Session->CardStates.IsValidIndex(Index))
		{
			const FOnokoArcanaReadingCardState& State = SpreadViewModel->Session->CardStates[Index];
			PositionLabel = State.PositionLabel;
			PositionKey = State.PositionKey.ToString();
			bSelected = State.bSelected;
		}
		else if (ActiveSpreadDefinition.Slots.IsValidIndex(Index))
		{
			const FOnokoArcanaSpreadSlotDefinition& Slot = ActiveSpreadDefinition.Slots[Index];
			PositionLabel = Slot.DisplayLabel;
			PositionKey = Slot.PositionKey.ToString();
			bSelected = Slot.bDefaultSelected;
		}

		if (UTextRenderComponent* TextComponent = LabelActor->GetTextRender())
		{
			TextComponent->SetText(FText::FromString(PositionKey.ToUpper()));
			TextComponent->SetTextRenderColor(bSelected ? FColor(255, 220, 118, 255) : FColor(214, 236, 255, 255));
			TextComponent->SetWorldSize(bSelected ? 19.0f : 17.0f);
		}
	}

	HideUnusedSpreadSlotLabels(Count);
}

void AOnokoArcanaTableController::HideUnusedSpreadCardActors(int32 FirstUnusedIndex)
{
	for (int32 Index = FMath::Max(0, FirstUnusedIndex); Index < SpreadCardActors.Num(); ++Index)
	{
		if (AOnokoArcanaCardActor* CardActor = SpreadCardActors[Index])
		{
			CardActor->SetActorHiddenInGame(true);
		}
	}
}

void AOnokoArcanaTableController::HideUnusedSpreadSlotLabels(int32 FirstUnusedIndex)
{
	for (int32 Index = FMath::Max(0, FirstUnusedIndex); Index < SpreadSlotLabelActors.Num(); ++Index)
	{
		if (ATextRenderActor* LabelActor = SpreadSlotLabelActors[Index])
		{
			LabelActor->SetActorHiddenInGame(true);
		}
	}
}

void AOnokoArcanaTableController::CaptureLastError()
{
	LastErrorMessage = ViewModel ? ViewModel->LastErrorMessage : FString();
}

void AOnokoArcanaTableController::CaptureLastSpreadError()
{
	LastErrorMessage = SpreadViewModel ? SpreadViewModel->LastErrorMessage : FString();
}
