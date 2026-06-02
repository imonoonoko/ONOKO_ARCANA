#include "OnokoArcanaSpreadReadingSession.h"

bool UOnokoArcanaSpreadReadingSession::InitializeMajorArcanaV5(FString& OutErrorMessage)
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

bool UOnokoArcanaSpreadReadingSession::StartNewReading(
	const FString& InQuestion,
	const FOnokoArcanaSpreadDefinition& InSpreadDefinition,
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

	if (!Deck || Deck->Cards.Num() == 0)
	{
		OutErrorMessage = TEXT("Deck is empty. Initialize the Major Arcana V5 deck before starting a spread reading.");
		return false;
	}

	if (InSpreadDefinition.SpreadId.IsNone() || InSpreadDefinition.Slots.Num() == 0)
	{
		OutErrorMessage = TEXT("A spread definition with at least one slot is required.");
		return false;
	}

	if (InSpreadDefinition.Slots.Num() > Deck->Cards.Num())
	{
		OutErrorMessage = FString::Printf(
			TEXT("Spread '%s' requires %d cards, but the current deck only has %d cards."),
			*InSpreadDefinition.SpreadId.ToString(),
			InSpreadDefinition.Slots.Num(),
			Deck->Cards.Num());
		return false;
	}

	Question = InQuestion;
	SpreadDefinition = InSpreadDefinition;
	CardStates.Reset(InSpreadDefinition.Slots.Num());
	bHasActiveReading = true;
	bHasDrawnSpread = false;
	SummaryNote.Reset();
	SelectedPositionKey = NAME_None;

	int32 DefaultSelectedIndex = INDEX_NONE;
	for (int32 Index = 0; Index < InSpreadDefinition.Slots.Num(); ++Index)
	{
		const FOnokoArcanaSpreadSlotDefinition& Slot = InSpreadDefinition.Slots[Index];
		CardStates.Add(MakeCardStateFromSlot(Slot));
		if (Slot.bDefaultSelected)
		{
			DefaultSelectedIndex = Index;
		}
	}

	SetSelectedIndex(DefaultSelectedIndex != INDEX_NONE ? DefaultSelectedIndex : 0);
	Deck->ResetDrawState(Seed, bUseSeed);
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::DrawSpread(bool bAllowReversed, FString& OutErrorMessage)
{
	if (!bHasActiveReading || CardStates.Num() == 0)
	{
		OutErrorMessage = TEXT("Start a spread reading before drawing cards.");
		return false;
	}

	if (!Deck)
	{
		OutErrorMessage = TEXT("Deck is not initialized.");
		return false;
	}

	if (Deck->GetRemainingCount() < CardStates.Num())
	{
		OutErrorMessage = FString::Printf(
			TEXT("Not enough cards remain in the deck for this spread. Need %d, remaining %d."),
			CardStates.Num(),
			Deck->GetRemainingCount());
		return false;
	}

	TArray<FOnokoArcanaReadingCardState> NewStates = CardStates;
	for (FOnokoArcanaReadingCardState& State : NewStates)
	{
		FOnokoArcanaDrawResult Draw;
		if (!Deck->DrawOne(Draw, bAllowReversed) || !Draw.bSuccess)
		{
			OutErrorMessage = FString::Printf(TEXT("Could not draw a card for slot: %s"), *State.PositionKey.ToString());
			return false;
		}

		State.Draw = Draw;
		State.bHasDraw = true;
		State.bRevealed = false;
		State.bGuideRevealed = false;
		State.UserInterpretation.Reset();
	}

	CardStates = MoveTemp(NewStates);
	bHasDrawnSpread = true;
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::SelectSlot(FName PositionKey, FString& OutErrorMessage)
{
	const int32 SlotIndex = FindSlotIndex(PositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutErrorMessage = FString::Printf(TEXT("Spread slot is out of range: %s"), *PositionKey.ToString());
		return false;
	}

	SetSelectedIndex(SlotIndex);
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::RevealSelected(FString& OutErrorMessage)
{
	const int32 SlotIndex = FindSlotIndex(SelectedPositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutErrorMessage = TEXT("Select a spread slot before revealing a card.");
		return false;
	}

	FOnokoArcanaReadingCardState& State = CardStates[SlotIndex];
	if (!State.bHasDraw || !State.Draw.bSuccess)
	{
		OutErrorMessage = TEXT("Draw the spread before revealing a selected slot.");
		return false;
	}

	State.bRevealed = true;
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::RevealNext(FString& OutErrorMessage)
{
	const int32 SlotIndex = FindNextRevealIndex();
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutErrorMessage = TEXT("There are no unrevealed drawn cards left in this spread.");
		return false;
	}

	SetSelectedIndex(SlotIndex);
	CardStates[SlotIndex].bRevealed = true;
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::SubmitSlotInterpretation(
	FName PositionKey,
	const FString& Text,
	FString& OutErrorMessage)
{
	const int32 SlotIndex = FindSlotIndex(PositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutErrorMessage = FString::Printf(TEXT("Spread slot is out of range: %s"), *PositionKey.ToString());
		return false;
	}

	CardStates[SlotIndex].UserInterpretation = Text;
	OutErrorMessage.Reset();
	return true;
}

bool UOnokoArcanaSpreadReadingSession::SubmitSelectedSlotInterpretation(const FString& Text, FString& OutErrorMessage)
{
	return SubmitSlotInterpretation(SelectedPositionKey, Text, OutErrorMessage);
}

void UOnokoArcanaSpreadReadingSession::SubmitSummaryNote(const FString& Text)
{
	SummaryNote = Text;
}

bool UOnokoArcanaSpreadReadingSession::RevealSelectedGuide(FString& OutErrorMessage)
{
	const int32 SlotIndex = FindSlotIndex(SelectedPositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutErrorMessage = TEXT("Select a spread slot before revealing guide meanings.");
		return false;
	}

	FOnokoArcanaReadingCardState& State = CardStates[SlotIndex];
	if (!State.bHasDraw || !State.Draw.bSuccess)
	{
		OutErrorMessage = TEXT("Draw the spread before revealing guide meanings.");
		return false;
	}

	if (!State.bRevealed)
	{
		OutErrorMessage = TEXT("Reveal the selected card before revealing guide meanings.");
		return false;
	}

	State.bGuideRevealed = true;
	OutErrorMessage.Reset();
	return true;
}

void UOnokoArcanaSpreadReadingSession::ResetReading()
{
	Question.Reset();
	SpreadDefinition = FOnokoArcanaSpreadDefinition();
	CardStates.Reset();
	SelectedPositionKey = NAME_None;
	SummaryNote.Reset();
	bHasActiveReading = false;
	bHasDrawnSpread = false;
}

bool UOnokoArcanaSpreadReadingSession::GetSelectedCardState(FOnokoArcanaReadingCardState& OutState) const
{
	const int32 SlotIndex = FindSlotIndex(SelectedPositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		OutState = FOnokoArcanaReadingCardState();
		return false;
	}

	OutState = CardStates[SlotIndex];
	return true;
}

FOnokoArcanaSpreadReadingState UOnokoArcanaSpreadReadingSession::GetReadingState() const
{
	FOnokoArcanaSpreadReadingState State;
	State.Question = Question;
	State.SpreadId = SpreadDefinition.SpreadId;
	State.SpreadDisplayName = SpreadDefinition.DisplayName;
	State.DeckId = Deck ? Deck->DeckId : FString();
	State.CardStates = CardStates;
	State.SelectedPositionKey = SelectedPositionKey;
	State.SummaryNote = SummaryNote;
	return State;
}

int32 UOnokoArcanaSpreadReadingSession::GetCardCount() const
{
	return CardStates.Num();
}

int32 UOnokoArcanaSpreadReadingSession::GetDrawnCount() const
{
	int32 Count = 0;
	for (const FOnokoArcanaReadingCardState& State : CardStates)
	{
		if (State.bHasDraw && State.Draw.bSuccess)
		{
			++Count;
		}
	}
	return Count;
}

int32 UOnokoArcanaSpreadReadingSession::GetRevealedCount() const
{
	int32 Count = 0;
	for (const FOnokoArcanaReadingCardState& State : CardStates)
	{
		if (State.bRevealed)
		{
			++Count;
		}
	}
	return Count;
}

bool UOnokoArcanaSpreadReadingSession::CanRevealNext() const
{
	return FindNextRevealIndex() != INDEX_NONE;
}

bool UOnokoArcanaSpreadReadingSession::CanRevealSelectedGuide() const
{
	const int32 SlotIndex = FindSlotIndex(SelectedPositionKey);
	if (!CardStates.IsValidIndex(SlotIndex))
	{
		return false;
	}

	const FOnokoArcanaReadingCardState& State = CardStates[SlotIndex];
	return State.bHasDraw && State.Draw.bSuccess && State.bRevealed;
}

int32 UOnokoArcanaSpreadReadingSession::FindSlotIndex(FName PositionKey) const
{
	for (int32 Index = 0; Index < CardStates.Num(); ++Index)
	{
		if (CardStates[Index].PositionKey == PositionKey)
		{
			return Index;
		}
	}
	return INDEX_NONE;
}

int32 UOnokoArcanaSpreadReadingSession::FindNextRevealIndex() const
{
	int32 BestIndex = INDEX_NONE;
	int32 BestRevealOrder = TNumericLimits<int32>::Max();
	for (int32 Index = 0; Index < CardStates.Num(); ++Index)
	{
		const FOnokoArcanaReadingCardState& State = CardStates[Index];
		if (State.bHasDraw && State.Draw.bSuccess && !State.bRevealed && State.RevealOrder < BestRevealOrder)
		{
			BestIndex = Index;
			BestRevealOrder = State.RevealOrder;
		}
	}
	return BestIndex;
}

void UOnokoArcanaSpreadReadingSession::SetSelectedIndex(int32 SelectedIndex)
{
	for (int32 Index = 0; Index < CardStates.Num(); ++Index)
	{
		const bool bSelected = Index == SelectedIndex;
		CardStates[Index].bSelected = bSelected;
		if (bSelected)
		{
			SelectedPositionKey = CardStates[Index].PositionKey;
		}
	}
}

FOnokoArcanaReadingCardState UOnokoArcanaSpreadReadingSession::MakeCardStateFromSlot(
	const FOnokoArcanaSpreadSlotDefinition& Slot)
{
	FOnokoArcanaReadingCardState State;
	State.PositionKey = Slot.PositionKey;
	State.PositionLabel = Slot.DisplayLabel;
	State.RevealOrder = Slot.RevealOrder;
	State.GuidePrompt = Slot.GuidePrompt;
	State.bSelected = Slot.bDefaultSelected;
	return State;
}
