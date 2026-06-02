#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaDeckRuntime.h"
#include "OnokoArcanaOneCardSession.generated.h"

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaOneCardSession : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	TObjectPtr<UOnokoArcanaDeckRuntime> Deck;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	FString Question;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	FOnokoArcanaDrawResult CurrentDraw;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	FString UserInterpretation;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	bool bHasCurrentDraw = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Session")
	bool bGuideRevealed = false;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	bool InitializeMajorArcanaV5(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	bool StartNewReading(const FString& InQuestion, int32 Seed, bool bUseSeed, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	bool DrawOne(bool bAllowReversed, FOnokoArcanaDrawResult& OutDraw, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	void SubmitUserInterpretation(const FString& InUserInterpretation);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	bool RevealGuide(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Session")
	void ResetReading();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Session")
	bool CanDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Session")
	bool CanRevealGuide() const;
};
