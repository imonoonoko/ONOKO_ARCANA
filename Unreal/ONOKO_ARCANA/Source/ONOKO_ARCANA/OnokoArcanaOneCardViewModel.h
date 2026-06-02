#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaDeckRuntime.h"
#include "OnokoArcanaOneCardViewModel.generated.h"

class UOnokoArcanaOneCardSession;

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaOneCardViewModel : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|ViewModel")
	TObjectPtr<UOnokoArcanaOneCardSession> Session;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|ViewModel")
	FString LastErrorMessage;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	bool Initialize();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	bool StartReading(const FString& Question, int32 Seed = 0, bool bUseSeed = false);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	bool DrawOne(bool bAllowReversed = true);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	void SubmitUserInterpretation(const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	bool RevealGuide();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|ViewModel")
	void ResetReading();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	bool HasCurrentDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	bool IsGuideRevealed() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FOnokoArcanaDrawResult GetCurrentDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FString GetCardTitle() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FString GetOrientationLabel() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FString GetActiveKeywordsText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FString GetStudyFocusText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	FString GetUserInterpretation() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	bool CanDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|ViewModel")
	bool CanRevealGuide() const;

private:
	UOnokoArcanaOneCardSession* EnsureSession();
};
