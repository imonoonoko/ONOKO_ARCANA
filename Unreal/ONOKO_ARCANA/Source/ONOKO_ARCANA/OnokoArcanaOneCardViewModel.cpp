#include "OnokoArcanaOneCardViewModel.h"

#include "OnokoArcanaOneCardSession.h"

bool UOnokoArcanaOneCardViewModel::Initialize()
{
	UOnokoArcanaOneCardSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create one-card session.");
		return false;
	}

	const bool bInitialized = ActiveSession->InitializeMajorArcanaV5(LastErrorMessage);
	return bInitialized;
}

bool UOnokoArcanaOneCardViewModel::StartReading(const FString& Question, int32 Seed, bool bUseSeed)
{
	UOnokoArcanaOneCardSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create one-card session.");
		return false;
	}

	if (!ActiveSession->Deck && !ActiveSession->InitializeMajorArcanaV5(LastErrorMessage))
	{
		return false;
	}

	return ActiveSession->StartNewReading(Question, Seed, bUseSeed, LastErrorMessage);
}

bool UOnokoArcanaOneCardViewModel::DrawOne(bool bAllowReversed)
{
	UOnokoArcanaOneCardSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create one-card session.");
		return false;
	}

	FOnokoArcanaDrawResult OutDraw;
	return ActiveSession->DrawOne(bAllowReversed, OutDraw, LastErrorMessage);
}

void UOnokoArcanaOneCardViewModel::SubmitUserInterpretation(const FString& Text)
{
	if (UOnokoArcanaOneCardSession* ActiveSession = EnsureSession())
	{
		ActiveSession->SubmitUserInterpretation(Text);
	}
}

bool UOnokoArcanaOneCardViewModel::RevealGuide()
{
	UOnokoArcanaOneCardSession* ActiveSession = EnsureSession();
	if (!ActiveSession)
	{
		LastErrorMessage = TEXT("Could not create one-card session.");
		return false;
	}

	return ActiveSession->RevealGuide(LastErrorMessage);
}

void UOnokoArcanaOneCardViewModel::ResetReading()
{
	if (Session)
	{
		Session->ResetReading();
	}
	LastErrorMessage.Reset();
}

bool UOnokoArcanaOneCardViewModel::HasCurrentDraw() const
{
	return Session && Session->bHasCurrentDraw;
}

bool UOnokoArcanaOneCardViewModel::IsGuideRevealed() const
{
	return Session && Session->bGuideRevealed;
}

FOnokoArcanaDrawResult UOnokoArcanaOneCardViewModel::GetCurrentDraw() const
{
	return Session ? Session->CurrentDraw : FOnokoArcanaDrawResult();
}

FString UOnokoArcanaOneCardViewModel::GetCardTitle() const
{
	if (!Session || !Session->bHasCurrentDraw)
	{
		return FString();
	}

	const FOnokoArcanaCardDefinition& Card = Session->CurrentDraw.Card;
	return FString::Printf(TEXT("%s %s / %s"), *Card.Number, *Card.JapaneseName, *Card.EnglishName);
}

FString UOnokoArcanaOneCardViewModel::GetOrientationLabel() const
{
	if (!Session || !Session->bHasCurrentDraw)
	{
		return FString();
	}

	return Session->CurrentDraw.Orientation == EOnokoArcanaCardOrientation::Reversed
		? TEXT("逆位置")
		: TEXT("正位置");
}

FString UOnokoArcanaOneCardViewModel::GetActiveKeywordsText() const
{
	if (!Session || !Session->bHasCurrentDraw)
	{
		return FString();
	}

	return FString::Join(Session->CurrentDraw.ActiveKeywords, TEXT(" / "));
}

FString UOnokoArcanaOneCardViewModel::GetStudyFocusText() const
{
	if (!Session || !Session->bHasCurrentDraw || !Session->bGuideRevealed)
	{
		return FString();
	}

	return Session->CurrentDraw.Card.StudyFocus;
}

FString UOnokoArcanaOneCardViewModel::GetUserInterpretation() const
{
	return Session ? Session->UserInterpretation : FString();
}

bool UOnokoArcanaOneCardViewModel::CanDraw() const
{
	return Session && Session->CanDraw();
}

bool UOnokoArcanaOneCardViewModel::CanRevealGuide() const
{
	return Session && Session->CanRevealGuide();
}

UOnokoArcanaOneCardSession* UOnokoArcanaOneCardViewModel::EnsureSession()
{
	if (!Session)
	{
		Session = NewObject<UOnokoArcanaOneCardSession>(this);
	}
	return Session;
}
