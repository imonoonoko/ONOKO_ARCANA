#include "OnokoArcanaSpreadReadingViewModel.h"

bool UOnokoArcanaSpreadReadingViewModel::Initialize()
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create spread reading session.");
		return false;
	}

	return ActiveSession->InitializeMajorArcanaV5(LastErrorMessage);
}

bool UOnokoArcanaSpreadReadingViewModel::StartReading(
	const FString& Question,
	const FOnokoArcanaSpreadDefinition& SpreadDefinition,
	int32 Seed,
	bool bUseSeed)
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create spread reading session.");
		return false;
	}

	if (!ActiveSession->Deck && !ActiveSession->InitializeMajorArcanaV5(LastErrorMessage))
	{
		return false;
	}

	return ActiveSession->StartNewReading(Question, SpreadDefinition, Seed, bUseSeed, LastErrorMessage);
}

bool UOnokoArcanaSpreadReadingViewModel::DrawSpread(bool bAllowReversed)
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->DrawSpread(bAllowReversed, LastErrorMessage) : false;
}

bool UOnokoArcanaSpreadReadingViewModel::SelectSlot(FName PositionKey)
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->SelectSlot(PositionKey, LastErrorMessage) : false;
}

bool UOnokoArcanaSpreadReadingViewModel::RevealSelected()
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->RevealSelected(LastErrorMessage) : false;
}

bool UOnokoArcanaSpreadReadingViewModel::RevealNext()
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->RevealNext(LastErrorMessage) : false;
}

bool UOnokoArcanaSpreadReadingViewModel::SubmitSelectedSlotInterpretation(const FString& Text)
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->SubmitSelectedSlotInterpretation(Text, LastErrorMessage) : false;
}

bool UOnokoArcanaSpreadReadingViewModel::SubmitSlotInterpretation(FName PositionKey, const FString& Text)
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->SubmitSlotInterpretation(PositionKey, Text, LastErrorMessage) : false;
}

void UOnokoArcanaSpreadReadingViewModel::SubmitSummaryNote(const FString& Text)
{
	if (UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession())
	{
		ActiveSession->SubmitSummaryNote(Text);
	}
}

bool UOnokoArcanaSpreadReadingViewModel::RevealSelectedGuide()
{
	UOnokoArcanaSpreadReadingSession* ActiveSession = EnsureSession();
	return ActiveSession ? ActiveSession->RevealSelectedGuide(LastErrorMessage) : false;
}

void UOnokoArcanaSpreadReadingViewModel::ResetReading()
{
	if (Session)
	{
		Session->ResetReading();
	}
	LastErrorMessage.Reset();
}

FString UOnokoArcanaSpreadReadingViewModel::GetProgressText() const
{
	if (!Session)
	{
		return FString();
	}

	return FString::Printf(TEXT("%d/%d revealed"), Session->GetRevealedCount(), Session->GetCardCount());
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedPositionLabel() const
{
	FOnokoArcanaReadingCardState State;
	return GetSelectedState(State) ? State.PositionLabel : FString();
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedCardTitle() const
{
	FOnokoArcanaReadingCardState State;
	if (!GetSelectedState(State) || !State.bHasDraw)
	{
		return FString();
	}

	const FOnokoArcanaCardDefinition& Card = State.Draw.Card;
	return FString::Printf(TEXT("%s %s / %s"), *Card.Number, *Card.JapaneseName, *Card.EnglishName);
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedOrientationLabel() const
{
	FOnokoArcanaReadingCardState State;
	if (!GetSelectedState(State) || !State.bHasDraw)
	{
		return FString();
	}

	return State.Draw.Orientation == EOnokoArcanaCardOrientation::Reversed ? TEXT("逆位置") : TEXT("正位置");
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedKeywordsText() const
{
	FOnokoArcanaReadingCardState State;
	if (!GetSelectedState(State) || !State.bHasDraw)
	{
		return FString();
	}

	return FString::Join(State.Draw.ActiveKeywords, TEXT(" / "));
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedGuideText() const
{
	FOnokoArcanaReadingCardState State;
	if (!GetSelectedState(State) || !State.bHasDraw || !State.bGuideRevealed)
	{
		return FString();
	}

	return State.Draw.Card.StudyFocus;
}

FString UOnokoArcanaSpreadReadingViewModel::GetSelectedUserInterpretation() const
{
	FOnokoArcanaReadingCardState State;
	return GetSelectedState(State) ? State.UserInterpretation : FString();
}

bool UOnokoArcanaSpreadReadingViewModel::HasDrawnSpread() const
{
	return Session && Session->bHasDrawnSpread;
}

bool UOnokoArcanaSpreadReadingViewModel::CanRevealNext() const
{
	return Session && Session->CanRevealNext();
}

bool UOnokoArcanaSpreadReadingViewModel::CanRevealSelectedGuide() const
{
	return Session && Session->CanRevealSelectedGuide();
}

UOnokoArcanaSpreadReadingSession* UOnokoArcanaSpreadReadingViewModel::EnsureSession()
{
	if (!Session)
	{
		Session = NewObject<UOnokoArcanaSpreadReadingSession>(this);
	}
	return Session;
}

bool UOnokoArcanaSpreadReadingViewModel::GetSelectedState(FOnokoArcanaReadingCardState& OutState) const
{
	return Session && Session->GetSelectedCardState(OutState);
}
