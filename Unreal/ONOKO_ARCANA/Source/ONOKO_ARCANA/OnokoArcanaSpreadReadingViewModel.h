#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaSpreadReadingSession.h"
#include "OnokoArcanaSpreadReadingViewModel.generated.h"

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaSpreadReadingViewModel : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread ViewModel")
	TObjectPtr<UOnokoArcanaSpreadReadingSession> Session;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread ViewModel")
	FString LastErrorMessage;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool Initialize();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool StartReading(const FString& Question, const FOnokoArcanaSpreadDefinition& SpreadDefinition, int32 Seed = 0, bool bUseSeed = false);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool DrawSpread(bool bAllowReversed = true);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool SelectSlot(FName PositionKey);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool RevealSelected();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool RevealNext();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool SubmitSelectedSlotInterpretation(const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool SubmitSlotInterpretation(FName PositionKey, const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	void SubmitSummaryNote(const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	bool RevealSelectedGuide();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread ViewModel")
	void ResetReading();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetProgressText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedPositionLabel() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedCardTitle() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedOrientationLabel() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedKeywordsText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedGuideText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	FString GetSelectedUserInterpretation() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	bool HasDrawnSpread() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	bool CanRevealNext() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread ViewModel")
	bool CanRevealSelectedGuide() const;

private:
	UOnokoArcanaSpreadReadingSession* EnsureSession();
	bool GetSelectedState(FOnokoArcanaReadingCardState& OutState) const;
};
