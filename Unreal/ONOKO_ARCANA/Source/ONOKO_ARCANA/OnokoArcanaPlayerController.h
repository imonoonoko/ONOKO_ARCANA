#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "OnokoArcanaPlayerController.generated.h"

class AOnokoArcanaTableController;
class AOnokoArcanaCardActor;
class ACameraActor;
class AStaticMeshActor;
class UOnokoArcanaTableHudWidget;

UCLASS(BlueprintType, Blueprintable)
class ONOKO_ARCANA_API AOnokoArcanaPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	AOnokoArcanaPlayerController();

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TSubclassOf<UOnokoArcanaTableHudWidget> TableHudWidgetClass;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UOnokoArcanaTableHudWidget> TableHudWidget;

	UPROPERTY(EditInstanceOnly, BlueprintReadWrite, Category = "ONOKO Arcana|HUD")
	TObjectPtr<AOnokoArcanaTableController> TableController;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|HUD")
	bool bAutoCreateTableHud = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|HUD")
	bool bUseGameAndUiInputMode = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	bool bAutoSpawnPhase1Actors = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FVector AutoSpawnCardLocation = FVector(0.0f, 0.0f, 8.0f);

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FRotator AutoSpawnCardRotation = FRotator::ZeroRotator;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FVector AutoSpawnControllerLocation = FVector(0.0f, 0.0f, 80.0f);

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	bool bHideExistingStaticMeshActorsForPhase1 = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	bool bAutoSpawnPhase1TableSurface = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FVector AutoSpawnTableLocation = FVector(0.0f, 0.0f, 0.0f);

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FVector AutoSpawnTableScale = FVector(7.0f, 5.0f, 1.0f);

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	bool bAutoSpawnPhase1Camera = true;

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FVector AutoSpawnCameraLocation = FVector(0.0f, 0.0f, 360.0f);

	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "ONOKO Arcana|Phase 1")
	FRotator AutoSpawnCameraRotation = FRotator(-90.0f, 0.0f, 0.0f);

	virtual void BeginPlay() override;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	bool FindTableControllerInWorld();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	bool CreateTableHud();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void RemoveTableHud();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SetTableController(AOnokoArcanaTableController* InTableController);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Phase 1")
	bool EnsurePhase1RuntimeActors();

private:
	AOnokoArcanaCardActor* FindReadingCardActorInWorld() const;
	void HideExistingStaticMeshActorsForPhase1() const;
	AStaticMeshActor* SpawnPhase1TableSurface();
	ACameraActor* EnsurePhase1Camera();
	void RunPhase4ThreeCardDemoIfRequested();
};
