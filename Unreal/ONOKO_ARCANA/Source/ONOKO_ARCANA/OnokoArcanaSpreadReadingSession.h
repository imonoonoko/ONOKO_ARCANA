#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaDeckRuntime.h"
#include "OnokoArcanaSpreadDefinition.h"
#include "OnokoArcanaSpreadReadingSession.generated.h"

USTRUCT(BlueprintType)
struct FOnokoArcanaReadingCardState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FName PositionKey;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString PositionLabel;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	int32 RevealOrder = 0;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString GuidePrompt;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FOnokoArcanaDrawResult Draw;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bHasDraw = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bRevealed = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bSelected = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString UserInterpretation;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bGuideRevealed = false;
};

USTRUCT(BlueprintType)
struct FOnokoArcanaSpreadReadingState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString Question;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FName SpreadId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString SpreadDisplayName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString DeckId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	TArray<FOnokoArcanaReadingCardState> CardStates;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FName SelectedPositionKey;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString SummaryNote;
};

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaSpreadReadingSession : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	TObjectPtr<UOnokoArcanaDeckRuntime> Deck;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString Question;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FOnokoArcanaSpreadDefinition SpreadDefinition;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	TArray<FOnokoArcanaReadingCardState> CardStates;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FName SelectedPositionKey;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	FString SummaryNote;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bHasActiveReading = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread Reading")
	bool bHasDrawnSpread = false;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool InitializeMajorArcanaV5(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool StartNewReading(
		const FString& InQuestion,
		const FOnokoArcanaSpreadDefinition& InSpreadDefinition,
		int32 Seed,
		bool bUseSeed,
		FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool DrawSpread(bool bAllowReversed, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool SelectSlot(FName PositionKey, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool RevealSelected(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool RevealNext(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool SubmitSlotInterpretation(FName PositionKey, const FString& Text, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool SubmitSelectedSlotInterpretation(const FString& Text, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	void SubmitSummaryNote(const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	bool RevealSelectedGuide(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread Reading")
	void ResetReading();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	bool GetSelectedCardState(FOnokoArcanaReadingCardState& OutState) const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	FOnokoArcanaSpreadReadingState GetReadingState() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	int32 GetCardCount() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	int32 GetDrawnCount() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	int32 GetRevealedCount() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	bool CanRevealNext() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread Reading")
	bool CanRevealSelectedGuide() const;

private:
	int32 FindSlotIndex(FName PositionKey) const;
	int32 FindNextRevealIndex() const;
	void SetSelectedIndex(int32 SelectedIndex);
	static FOnokoArcanaReadingCardState MakeCardStateFromSlot(const FOnokoArcanaSpreadSlotDefinition& Slot);
};
