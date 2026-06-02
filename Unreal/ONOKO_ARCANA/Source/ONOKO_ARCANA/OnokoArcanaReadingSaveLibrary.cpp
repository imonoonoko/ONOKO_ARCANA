#include "OnokoArcanaReadingSaveLibrary.h"

#include "Kismet/GameplayStatics.h"
#include "Misc/Guid.h"
#include "OnokoArcanaOneCardSession.h"
#include "OnokoArcanaSpreadReadingSession.h"

namespace
{
FString OrientationToLabel(EOnokoArcanaCardOrientation Orientation)
{
	return Orientation == EOnokoArcanaCardOrientation::Reversed ? TEXT("逆位置") : TEXT("正位置");
}

FString NormalizeSlotName(const FString& SlotName)
{
	return SlotName.IsEmpty() ? TEXT("ONOKO_ARCANA_Readings") : SlotName;
}

FOnokoArcanaSavedReadingCardState MakeSavedCardState(
	const FString& PositionKey,
	const FString& PositionLabel,
	int32 RevealOrder,
	const FOnokoArcanaDrawResult& Draw,
	const FString& UserInterpretation,
	bool bRevealed,
	bool bGuideRevealed)
{
	FOnokoArcanaSavedReadingCardState SavedState;
	SavedState.PositionKey = PositionKey;
	SavedState.PositionLabel = PositionLabel;
	SavedState.RevealOrder = RevealOrder;
	if (Draw.bSuccess)
	{
		SavedState.CardId = Draw.Card.Id;
		SavedState.CardNumber = Draw.Card.Number;
		SavedState.EnglishName = Draw.Card.EnglishName;
		SavedState.JapaneseName = Draw.Card.JapaneseName;
		SavedState.OrientationLabel = OrientationToLabel(Draw.Orientation);
		SavedState.ActiveKeywords = Draw.ActiveKeywords;
		SavedState.StudyFocus = Draw.Card.StudyFocus;
	}
	SavedState.UserInterpretation = UserInterpretation;
	SavedState.bRevealed = bRevealed;
	SavedState.bGuideRevealed = bGuideRevealed;
	return SavedState;
}
}

bool UOnokoArcanaReadingSaveLibrary::MakeSavedReadingFromSession(
	const UOnokoArcanaOneCardSession* Session,
	FOnokoArcanaSavedReading& OutReading,
	FString& OutErrorMessage)
{
	OutReading = FOnokoArcanaSavedReading();
	if (!Session || !Session->bHasCurrentDraw || !Session->CurrentDraw.bSuccess)
	{
		OutErrorMessage = TEXT("A completed one-card draw is required before saving a reading.");
		return false;
	}

	const FOnokoArcanaDrawResult& Draw = Session->CurrentDraw;
	OutReading.ReadingId = FGuid::NewGuid().ToString(EGuidFormats::DigitsWithHyphens);
	OutReading.CreatedAtUtc = FDateTime::UtcNow();
	OutReading.Question = Session->Question;
	OutReading.CardId = Draw.Card.Id;
	OutReading.CardNumber = Draw.Card.Number;
	OutReading.EnglishName = Draw.Card.EnglishName;
	OutReading.JapaneseName = Draw.Card.JapaneseName;
	OutReading.OrientationLabel = OrientationToLabel(Draw.Orientation);
	OutReading.ActiveKeywords = Draw.ActiveKeywords;
	OutReading.StudyFocus = Draw.Card.StudyFocus;
	OutReading.UserInterpretation = Session->UserInterpretation;
	OutReading.bGuideRevealed = Session->bGuideRevealed;
	OutReading.CardStates.Add(MakeSavedCardState(
		OutReading.PositionKey,
		OutReading.PositionLabel,
		1,
		Draw,
		Session->UserInterpretation,
		true,
		Session->bGuideRevealed));
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaReadingSaveLibrary::MakeSavedReadingFromSpreadSession(
	const UOnokoArcanaSpreadReadingSession* Session,
	FOnokoArcanaSavedReading& OutReading,
	FString& OutErrorMessage)
{
	OutReading = FOnokoArcanaSavedReading();
	if (!Session || !Session->bHasActiveReading || !Session->bHasDrawnSpread || Session->CardStates.Num() == 0)
	{
		OutErrorMessage = TEXT("A drawn spread reading is required before saving.");
		return false;
	}

	FOnokoArcanaReadingCardState SummaryState;
	if (!Session->GetSelectedCardState(SummaryState) || !SummaryState.bHasDraw)
	{
		SummaryState = Session->CardStates[0];
	}

	if (!SummaryState.bHasDraw || !SummaryState.Draw.bSuccess)
	{
		OutErrorMessage = TEXT("A spread reading with at least one drawn card is required before saving.");
		return false;
	}

	OutReading.ReadingId = FGuid::NewGuid().ToString(EGuidFormats::DigitsWithHyphens);
	OutReading.CreatedAtUtc = FDateTime::UtcNow();
	OutReading.Question = Session->Question;
	OutReading.SpreadId = Session->SpreadDefinition.SpreadId.ToString();
	OutReading.SpreadDisplayName = Session->SpreadDefinition.DisplayName;
	OutReading.CardCount = Session->CardStates.Num();
	OutReading.PositionKey = SummaryState.PositionKey.ToString();
	OutReading.PositionLabel = SummaryState.PositionLabel;
	OutReading.CardId = SummaryState.Draw.Card.Id;
	OutReading.CardNumber = SummaryState.Draw.Card.Number;
	OutReading.EnglishName = SummaryState.Draw.Card.EnglishName;
	OutReading.JapaneseName = SummaryState.Draw.Card.JapaneseName;
	OutReading.OrientationLabel = OrientationToLabel(SummaryState.Draw.Orientation);
	OutReading.ActiveKeywords = SummaryState.Draw.ActiveKeywords;
	OutReading.StudyFocus = SummaryState.Draw.Card.StudyFocus;
	OutReading.UserInterpretation = Session->SummaryNote;
	OutReading.bGuideRevealed = SummaryState.bGuideRevealed;

	OutReading.CardStates.Reserve(Session->CardStates.Num());
	for (const FOnokoArcanaReadingCardState& State : Session->CardStates)
	{
		if (!State.bHasDraw || !State.Draw.bSuccess)
		{
			OutErrorMessage = FString::Printf(TEXT("Cannot save spread because slot '%s' has no drawn card."), *State.PositionKey.ToString());
			OutReading = FOnokoArcanaSavedReading();
			return false;
		}

		OutReading.CardStates.Add(MakeSavedCardState(
			State.PositionKey.ToString(),
			State.PositionLabel,
			State.RevealOrder,
			State.Draw,
			State.UserInterpretation,
			State.bRevealed,
			State.bGuideRevealed));
	}

	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaReadingSaveLibrary::SaveReadingToSlot(
	const FOnokoArcanaSavedReading& Reading,
	const FString& SlotName,
	int32 UserIndex,
	FString& OutErrorMessage)
{
	if (Reading.CardId.IsEmpty())
	{
		OutErrorMessage = TEXT("Cannot save an empty reading.");
		return false;
	}

	const FString EffectiveSlotName = NormalizeSlotName(SlotName);
	UOnokoArcanaReadingSaveGame* SaveGame = nullptr;
	if (UGameplayStatics::DoesSaveGameExist(EffectiveSlotName, UserIndex))
	{
		SaveGame = Cast<UOnokoArcanaReadingSaveGame>(
			UGameplayStatics::LoadGameFromSlot(EffectiveSlotName, UserIndex));
	}

	if (!SaveGame)
	{
		SaveGame = Cast<UOnokoArcanaReadingSaveGame>(
			UGameplayStatics::CreateSaveGameObject(UOnokoArcanaReadingSaveGame::StaticClass()));
	}

	if (!SaveGame)
	{
		OutErrorMessage = TEXT("Could not create reading SaveGame object.");
		return false;
	}

	SaveGame->Readings.Insert(Reading, 0);
	if (!UGameplayStatics::SaveGameToSlot(SaveGame, EffectiveSlotName, UserIndex))
	{
		OutErrorMessage = FString::Printf(TEXT("Could not save readings to slot: %s"), *EffectiveSlotName);
		return false;
	}

	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaReadingSaveLibrary::LoadReadingsFromSlot(
	const FString& SlotName,
	int32 UserIndex,
	UOnokoArcanaReadingSaveGame*& OutSaveGame,
	FString& OutErrorMessage)
{
	const FString EffectiveSlotName = NormalizeSlotName(SlotName);
	OutSaveGame = nullptr;
	if (!UGameplayStatics::DoesSaveGameExist(EffectiveSlotName, UserIndex))
	{
		OutSaveGame = Cast<UOnokoArcanaReadingSaveGame>(
			UGameplayStatics::CreateSaveGameObject(UOnokoArcanaReadingSaveGame::StaticClass()));
		OutErrorMessage.Reset();
		return OutSaveGame != nullptr;
	}

	OutSaveGame = Cast<UOnokoArcanaReadingSaveGame>(
		UGameplayStatics::LoadGameFromSlot(EffectiveSlotName, UserIndex));
	if (!OutSaveGame)
	{
		OutErrorMessage = FString::Printf(TEXT("Could not load readings from slot: %s"), *EffectiveSlotName);
		return false;
	}

	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaReadingSaveLibrary::DeleteReadingsSlot(const FString& SlotName, int32 UserIndex)
{
	const FString EffectiveSlotName = NormalizeSlotName(SlotName);
	if (!UGameplayStatics::DoesSaveGameExist(EffectiveSlotName, UserIndex))
	{
		return true;
	}
	return UGameplayStatics::DeleteGameInSlot(EffectiveSlotName, UserIndex);
}
