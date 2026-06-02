#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaReadingSaveGame.h"
#include "OnokoArcanaReadingHistoryViewModel.generated.h"

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaReadingHistoryViewModel : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|History")
	TObjectPtr<UOnokoArcanaReadingSaveGame> SaveGame;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|History")
	int32 SelectedIndex = INDEX_NONE;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|History")
	FString LastErrorMessage;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	bool LoadFromSlot(const FString& SlotName, int32 UserIndex);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	void SetSaveGame(UOnokoArcanaReadingSaveGame* InSaveGame);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	bool SelectReading(int32 Index);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	void ClearSelection();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	bool HasHistory() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	int32 GetReadingCount() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	int32 GetSelectedIndex() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FOnokoArcanaSavedReading GetSelectedReading() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FString GetEmptyStateText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FString GetReadingSummary(int32 Index) const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FString GetLatestReadingSummary() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FString GetSelectedTitleText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|History")
	FString GetSelectedDetailText() const;

private:
	const FOnokoArcanaSavedReading* GetReadingPtr(int32 Index) const;
	static FString FormatReadingSummary(const FOnokoArcanaSavedReading& Reading);
	static FString FormatReadingDetail(const FOnokoArcanaSavedReading& Reading);
};
