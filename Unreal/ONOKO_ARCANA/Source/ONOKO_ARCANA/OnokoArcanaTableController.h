#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "OnokoArcanaDeckRuntime.h"
#include "OnokoArcanaSpreadDefinition.h"
#include "OnokoArcanaTableController.generated.h"

class AOnokoArcanaCardActor;
class ATextRenderActor;
class UOnokoArcanaReadingHistoryViewModel;
class UOnokoArcanaReadingSaveGame;
class UOnokoArcanaOneCardViewModel;
class UOnokoArcanaSpreadRegistry;
class UOnokoArcanaSpreadReadingViewModel;

UCLASS(BlueprintType)
class ONOKO_ARCANA_API AOnokoArcanaTableController : public AActor
{
	GENERATED_BODY()

public:
	AOnokoArcanaTableController();

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Table")
	TObjectPtr<AOnokoArcanaCardActor> ReadingCardActor;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Table")
	TObjectPtr<UOnokoArcanaOneCardViewModel> ViewModel;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|History")
	TObjectPtr<UOnokoArcanaReadingHistoryViewModel> HistoryViewModel;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TObjectPtr<UOnokoArcanaSpreadReadingViewModel> SpreadViewModel;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TObjectPtr<UOnokoArcanaSpreadRegistry> SpreadRegistry;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TArray<TObjectPtr<AOnokoArcanaCardActor>> SpreadCardActors;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TArray<TObjectPtr<ATextRenderActor>> SpreadSlotLabelActors;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FName ActiveSpreadId = TEXT("one_card");

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FOnokoArcanaSpreadDefinition ActiveSpreadDefinition;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Table")
	FString DefaultQuestion;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Table")
	bool bAllowReversed = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Table")
	bool bUseDeterministicSeed = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Table")
	int32 DeterministicSeed = 12345;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Spread")
	float SpreadCardSpacingCentimeters = 100.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Spread")
	float SpreadCardCenterYOffsetCentimeters = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Spread")
	float SpreadLabelXOffsetCentimeters = -88.0f;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Table")
	FString LastErrorMessage;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Save")
	FString SaveSlotName = TEXT("ONOKO_ARCANA_Readings");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Save")
	int32 SaveUserIndex = 0;

	virtual void BeginPlay() override;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	bool InitializeTable();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread")
	bool InitializeSpreadRegistry();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread")
	bool SelectSpread(FName SpreadId);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread")
	bool SelectSpreadSlot(FName PositionKey);

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	TArray<FOnokoArcanaSpreadDefinition> GetAvailableSpreads() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FOnokoArcanaSpreadDefinition GetActiveSpread() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetActiveSpreadDisplayText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetActiveSpreadSlotListText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetAvailableSpreadListText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetSelectedSpreadSlotText() const;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	bool StartReading(const FString& Question);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	bool DrawCard(bool bRevealImmediately = false);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	bool RevealCard();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	void SubmitUserInterpretation(const FString& Text);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	bool RevealGuide();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Table")
	void ResetTable();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	bool SaveCurrentReading();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	bool LoadReadingHistory(UOnokoArcanaReadingSaveGame*& OutSaveGame);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	bool RefreshReadingHistory();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|History")
	bool SelectHistoryReading(int32 Index);

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Table")
	FOnokoArcanaDrawResult GetCurrentDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Table")
	bool HasCurrentDraw() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	bool IsOneCardSpread() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	bool IsSpreadReadingActive() const;

	UFUNCTION(BlueprintImplementableEvent, Category = "ONOKO Arcana|Table")
	void OnTableStateChanged();

	UFUNCTION(BlueprintImplementableEvent, Category = "ONOKO Arcana|Table")
	void OnCardDrawn(const FOnokoArcanaDrawResult& DrawResult);

private:
	UOnokoArcanaSpreadRegistry* EnsureSpreadRegistry();
	UOnokoArcanaOneCardViewModel* EnsureViewModel();
	UOnokoArcanaSpreadReadingViewModel* EnsureSpreadViewModel();
	UOnokoArcanaReadingHistoryViewModel* EnsureHistoryViewModel();
	bool SyncCardActorToViewModel(bool bRevealImmediately);
	bool EnsureSpreadCardActors(int32 RequiredCount);
	bool SyncSpreadCardActors();
	bool EnsureSpreadSlotLabels(int32 RequiredCount);
	void PlaceSpreadCardActors();
	void SyncSpreadSlotLabels();
	void HideUnusedSpreadCardActors(int32 FirstUnusedIndex);
	void HideUnusedSpreadSlotLabels(int32 FirstUnusedIndex);
	void CaptureLastError();
	void CaptureLastSpreadError();
};
