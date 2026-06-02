#include "OnokoArcanaOneCardSession.h"

bool UOnokoArcanaOneCardSession::InitializeMajorArcanaV5(FString& OutErrorMessage)
{
	if (!Deck)
	{
		Deck = NewObject<UOnokoArcanaDeckRuntime>(this);
	}

	const bool bLoaded = Deck->LoadMajorArcanaV5Manifest(OutErrorMessage);
	if (!bLoaded)
	{
		ResetReading();
		return false;
	}

	ResetReading();
	return true;
}

bool UOnokoArcanaOneCardSession::StartNewReading(
	const FString& InQuestion,
	int32 Seed,
	bool bUseSeed,
	FString& OutErrorMessage)
{
	if (!Deck)
	{
		if (!InitializeMajorArcanaV5(OutErrorMessage))
		{
			return false;
		}
	}

	if (Deck->Cards.Num() == 0)
	{
		OutErrorMessage = TEXT("Deck is empty. Initialize the Major Arcana V5 deck before starting a reading.");
		return false;
	}

	Question = InQuestion;
	UserInterpretation.Reset();
	bHasCurrentDraw = false;
	bGuideRevealed = false;
	CurrentDraw = FOnokoArcanaDrawResult();
	Deck->ResetDrawState(Seed, bUseSeed);
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaOneCardSession::DrawOne(
	bool bAllowReversed,
	FOnokoArcanaDrawResult& OutDraw,
	FString& OutErrorMessage)
{
	OutDraw = FOnokoArcanaDrawResult();
	if (!Deck)
	{
		OutErrorMessage = TEXT("Deck is not initialized.");
		return false;
	}

	if (!Deck->DrawOne(OutDraw, bAllowReversed) || !OutDraw.bSuccess)
	{
		OutErrorMessage = TEXT("Could not draw a card from the current deck.");
		return false;
	}

	CurrentDraw = OutDraw;
	bHasCurrentDraw = true;
	bGuideRevealed = false;
	OutErrorMessage.Reset();
	return true;
}

void UOnokoArcanaOneCardSession::SubmitUserInterpretation(const FString& InUserInterpretation)
{
	UserInterpretation = InUserInterpretation;
}

bool UOnokoArcanaOneCardSession::RevealGuide(FString& OutErrorMessage)
{
	if (!CanRevealGuide())
	{
		OutErrorMessage = TEXT("Draw a card before revealing guide meanings.");
		return false;
	}

	bGuideRevealed = true;
	OutErrorMessage.Reset();
	return true;
}

void UOnokoArcanaOneCardSession::ResetReading()
{
	Question.Reset();
	CurrentDraw = FOnokoArcanaDrawResult();
	UserInterpretation.Reset();
	bHasCurrentDraw = false;
	bGuideRevealed = false;
}

bool UOnokoArcanaOneCardSession::CanDraw() const
{
	return Deck && Deck->GetRemainingCount() > 0;
}

bool UOnokoArcanaOneCardSession::CanRevealGuide() const
{
	return bHasCurrentDraw && CurrentDraw.bSuccess;
}
