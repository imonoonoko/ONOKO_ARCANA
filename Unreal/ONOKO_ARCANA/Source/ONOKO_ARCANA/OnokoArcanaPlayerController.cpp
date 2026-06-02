#include "OnokoArcanaPlayerController.h"

#include "Blueprint/UserWidget.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Components/LightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "EngineUtils.h"
#include "Engine/PointLight.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Materials/MaterialInterface.h"
#include "OnokoArcanaCardActor.h"
#include "OnokoArcanaTableController.h"
#include "OnokoArcanaTableHudWidget.h"

AOnokoArcanaPlayerController::AOnokoArcanaPlayerController()
{
	TableHudWidgetClass = UOnokoArcanaTableHudWidget::StaticClass();
}

void AOnokoArcanaPlayerController::BeginPlay()
{
	Super::BeginPlay();

	FindTableControllerInWorld();
	if (bAutoSpawnPhase1Actors)
	{
		EnsurePhase1RuntimeActors();
	}
	if (bAutoCreateTableHud)
	{
		CreateTableHud();
	}
	RunPhase4ThreeCardDemoIfRequested();
}

bool AOnokoArcanaPlayerController::FindTableControllerInWorld()
{
	if (TableController)
	{
		return true;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	for (TActorIterator<AOnokoArcanaTableController> It(World); It; ++It)
	{
		TableController = *It;
		return true;
	}

	return false;
}

bool AOnokoArcanaPlayerController::CreateTableHud()
{
	if (TableHudWidget)
	{
		return true;
	}

	if (!TableHudWidgetClass)
	{
		return false;
	}

	TableHudWidget = CreateWidget<UOnokoArcanaTableHudWidget>(this, TableHudWidgetClass);
	if (!TableHudWidget)
	{
		return false;
	}

	if (!TableController)
	{
		FindTableControllerInWorld();
	}

	TableHudWidget->SetTableController(TableController);
	TableHudWidget->AddToViewport();

	if (bUseGameAndUiInputMode)
	{
		FInputModeGameAndUI InputMode;
		InputMode.SetHideCursorDuringCapture(false);
		SetInputMode(InputMode);
		bShowMouseCursor = true;
	}

	return true;
}

void AOnokoArcanaPlayerController::RemoveTableHud()
{
	if (TableHudWidget)
	{
		TableHudWidget->RemoveFromParent();
		TableHudWidget = nullptr;
	}
}

void AOnokoArcanaPlayerController::SetTableController(AOnokoArcanaTableController* InTableController)
{
	TableController = InTableController;
	if (TableHudWidget)
	{
		TableHudWidget->SetTableController(TableController);
	}
}

bool AOnokoArcanaPlayerController::EnsurePhase1RuntimeActors()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Ensuring runtime Phase 1 actors."));

	if (bHideExistingStaticMeshActorsForPhase1)
	{
		HideExistingStaticMeshActorsForPhase1();
	}

	if (bAutoSpawnPhase1TableSurface)
	{
		UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Runtime table surface is skipped for the current functional proof."));
	}

	FActorSpawnParameters LightSpawnParams;
	LightSpawnParams.Name = TEXT("BP_Auto_Phase1PointLight");
	if (APointLight* Light = World->SpawnActor<APointLight>(
			APointLight::StaticClass(),
			FVector(0.0f, 0.0f, 260.0f),
			FRotator::ZeroRotator,
			LightSpawnParams))
	{
		if (ULightComponent* LightComponent = Light->GetLightComponent())
		{
			LightComponent->SetIntensity(5000.0f);
		}
		UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Spawned runtime phase light."));
	}

	AOnokoArcanaCardActor* ReadingCardActor = FindReadingCardActorInWorld();
	if (!ReadingCardActor)
	{
		FActorSpawnParameters CardSpawnParams;
		CardSpawnParams.Name = TEXT("BP_Auto_Phase1ReadingCard");
		ReadingCardActor = World->SpawnActor<AOnokoArcanaCardActor>(
			AOnokoArcanaCardActor::StaticClass(),
			AutoSpawnCardLocation,
			AutoSpawnCardRotation,
			CardSpawnParams);
		UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Spawned runtime reading card actor."));
	}

	if (ReadingCardActor)
	{
		ReadingCardActor->SetActorLocation(AutoSpawnCardLocation);
		ReadingCardActor->SetActorRotation(FRotator(0.0f, 90.0f, 0.0f));
		ReadingCardActor->ConfigureCardScale(96.0f, 144.0f);
		ReadingCardActor->SetActorHiddenInGame(false);
		if (ReadingCardActor->CardPlane)
		{
			ReadingCardActor->CardPlane->SetVisibility(true, true);
			ReadingCardActor->CardPlane->SetHiddenInGame(false, true);
		}
		UE_LOG(
			LogTemp,
			Display,
			TEXT("[ONOKO_ARCANA_PHASE1] Runtime reading card placed at %s."),
			*ReadingCardActor->GetActorLocation().ToString());
	}

	if (!TableController)
	{
		FindTableControllerInWorld();
	}

	if (!TableController)
	{
		FActorSpawnParameters ControllerSpawnParams;
		ControllerSpawnParams.Name = TEXT("BP_Auto_Phase1TableController");
		TableController = World->SpawnActor<AOnokoArcanaTableController>(
			AOnokoArcanaTableController::StaticClass(),
			AutoSpawnControllerLocation,
			FRotator::ZeroRotator,
			ControllerSpawnParams);
		UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Spawned runtime table controller."));
	}

	if (!TableController)
	{
		return false;
	}

	if (ReadingCardActor && !TableController->ReadingCardActor)
	{
		TableController->ReadingCardActor = ReadingCardActor;
		TableController->DefaultQuestion = TEXT("今の自分に必要な視点は？");
		TableController->InitializeTable();
	}

	if (bAutoSpawnPhase1Camera)
	{
		if (ACameraActor* CameraActor = EnsurePhase1Camera())
		{
			SetViewTargetWithBlend(CameraActor, 0.0f);
			UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Assigned runtime phase camera."));
		}
	}

	return TableController && TableController->ReadingCardActor;
}

AOnokoArcanaCardActor* AOnokoArcanaPlayerController::FindReadingCardActorInWorld() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return nullptr;
	}

	for (TActorIterator<AOnokoArcanaCardActor> It(World); It; ++It)
	{
		return *It;
	}

	return nullptr;
}

void AOnokoArcanaPlayerController::HideExistingStaticMeshActorsForPhase1() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	int32 HiddenComponentCount = 0;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor || Actor->IsA<AOnokoArcanaCardActor>() || Actor->IsA<ACameraActor>())
		{
			continue;
		}

		TArray<UStaticMeshComponent*> MeshComponents;
		Actor->GetComponents<UStaticMeshComponent>(MeshComponents);
		for (UStaticMeshComponent* MeshComponent : MeshComponents)
		{
			if (!MeshComponent)
			{
				continue;
			}
			MeshComponent->SetVisibility(false, true);
			MeshComponent->SetHiddenInGame(true, true);
			MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			++HiddenComponentCount;
		}
	}

	UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Hidden %d existing static mesh components for PIE cleanup."), HiddenComponentCount);
}

AStaticMeshActor* AOnokoArcanaPlayerController::SpawnPhase1TableSurface()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return nullptr;
	}

	FActorSpawnParameters SpawnParams;
	SpawnParams.Name = TEXT("BP_Auto_Phase1TableSurface");
	AStaticMeshActor* TableActor = World->SpawnActor<AStaticMeshActor>(
		AStaticMeshActor::StaticClass(),
		AutoSpawnTableLocation,
		FRotator::ZeroRotator,
		SpawnParams);
	if (!TableActor)
	{
		return nullptr;
	}

	UStaticMesh* PlaneMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Plane.Plane"));
	if (UStaticMeshComponent* MeshComponent = TableActor->GetStaticMeshComponent())
	{
		MeshComponent->SetStaticMesh(PlaneMesh);
		MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		if (UMaterialInterface* TableMaterial = LoadObject<UMaterialInterface>(
				nullptr,
				TEXT("/Game/ONOKOArcana/Phase1/Materials/M_Phase1_Black_Acrylic_Mat.M_Phase1_Black_Acrylic_Mat")))
		{
			MeshComponent->SetMaterial(0, TableMaterial);
		}
	}

	TableActor->SetActorScale3D(AutoSpawnTableScale);
	UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Spawned runtime table surface."));

	return TableActor;
}

ACameraActor* AOnokoArcanaPlayerController::EnsurePhase1Camera()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return nullptr;
	}

	for (TActorIterator<ACameraActor> It(World); It; ++It)
	{
		ACameraActor* ExistingCamera = *It;
		if (ExistingCamera && ExistingCamera->GetFName() == TEXT("BP_Auto_Phase1Camera"))
		{
			return ExistingCamera;
		}
	}

	FActorSpawnParameters SpawnParams;
	SpawnParams.Name = TEXT("BP_Auto_Phase1Camera");
	ACameraActor* CameraActor = World->SpawnActor<ACameraActor>(
		ACameraActor::StaticClass(),
		AutoSpawnCameraLocation,
		AutoSpawnCameraRotation,
		SpawnParams);
	if (CameraActor)
	{
		if (UCameraComponent* CameraComponent = CameraActor->GetCameraComponent())
		{
			CameraComponent->SetProjectionMode(ECameraProjectionMode::Orthographic);
			CameraComponent->SetOrthoWidth(520.0f);
		}
		UE_LOG(LogTemp, Display, TEXT("[ONOKO_ARCANA_PHASE1] Spawned orthographic runtime phase camera."));
	}

	return CameraActor;
}

void AOnokoArcanaPlayerController::RunPhase4ThreeCardDemoIfRequested()
{
	if (!FParse::Param(FCommandLine::Get(), TEXT("ONOKOArcanaAutoThreeCardDemo")))
	{
		return;
	}

	if (!TableController)
	{
		FindTableControllerInWorld();
	}
	if (!TableController)
	{
		return;
	}

	TableController->SelectSpread(FName(TEXT("three_card_past_present_future")));
	TableController->StartReading(TEXT("この流れの過去・現在・未来を読む"));
	TableController->DrawCard(false);
	TableController->RevealCard();
	TableController->RevealCard();
	TableController->RevealCard();
	TableController->SubmitUserInterpretation(TEXT("未来の位置を中心に、流れ全体を確認する。"));
	TableController->RevealGuide();

	if (TableHudWidget)
	{
		TableHudWidget->RefreshFromController();
	}
}
