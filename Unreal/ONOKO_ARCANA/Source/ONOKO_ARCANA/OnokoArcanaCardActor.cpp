#include "OnokoArcanaCardActor.h"

#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "UObject/ConstructorHelpers.h"

AOnokoArcanaCardActor::AOnokoArcanaCardActor()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	CardPlane = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CardPlane"));
	CardPlane->SetupAttachment(Root);
	CardPlane->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	CardPlane->SetGenerateOverlapEvents(false);
	CardPlane->SetCastShadow(false);

	static ConstructorHelpers::FObjectFinder<UStaticMesh> PlaneMesh(TEXT("/Engine/BasicShapes/Plane.Plane"));
	if (PlaneMesh.Succeeded())
	{
		CardPlane->SetStaticMesh(PlaneMesh.Object);
	}

	static ConstructorHelpers::FObjectFinder<UMaterialInterface> CardMaterialAsset(
		TEXT("/Game/ONOKOArcana/Phase1/Materials/M_Phase1_CardMasked_TextureParam.M_Phase1_CardMasked_TextureParam"));
	if (CardMaterialAsset.Succeeded())
	{
		CardMaterialBase = CardMaterialAsset.Object;
	}

	ApplyCardScale();
}

void AOnokoArcanaCardActor::ConfigureCardScale(float WidthCentimeters, float HeightCentimeters)
{
	CardWidthCentimeters = FMath::Max(1.0f, WidthCentimeters);
	CardHeightCentimeters = FMath::Max(1.0f, HeightCentimeters);
	ApplyCardScale();
}

bool AOnokoArcanaCardActor::SetBackTexture(TSoftObjectPtr<UTexture2D> InBackTexture)
{
	BackTexture = InBackTexture;
	if (!bFaceUp)
	{
		return ApplyVisual();
	}
	return true;
}

bool AOnokoArcanaCardActor::SetCard(
	const FOnokoArcanaCardDefinition& InCard,
	EOnokoArcanaCardOrientation InOrientation,
	bool bRevealImmediately)
{
	CurrentCard = InCard;
	CurrentOrientation = InOrientation;
	bFaceUp = bRevealImmediately;
	return ApplyVisual();
}

bool AOnokoArcanaCardActor::ShowBack()
{
	bFaceUp = false;
	return ApplyVisual();
}

bool AOnokoArcanaCardActor::RevealFront()
{
	if (CurrentCard.Texture.IsNull())
	{
		return false;
	}

	bFaceUp = true;
	return ApplyVisual();
}

bool AOnokoArcanaCardActor::ApplyVisual()
{
	if (!CardPlane || !CardMaterialBase)
	{
		return false;
	}

	UTexture2D* Texture = ResolveCurrentTexture();
	if (!Texture)
	{
		return false;
	}

	if (!DynamicCardMaterial || DynamicCardMaterial->Parent != CardMaterialBase)
	{
		DynamicCardMaterial = UMaterialInstanceDynamic::Create(CardMaterialBase, this);
		CardPlane->SetMaterial(0, DynamicCardMaterial);
	}

	DynamicCardMaterial->SetTextureParameterValue(CardTextureParameterName, Texture);
	const float ReversedYaw = bFaceUp && CurrentOrientation == EOnokoArcanaCardOrientation::Reversed ? 180.0f : 0.0f;
	CardPlane->SetRelativeRotation(FRotator(0.0f, ReversedYaw, 0.0f));
	return true;
}

void AOnokoArcanaCardActor::ApplyCardScale()
{
	if (!CardPlane)
	{
		return;
	}

	CardPlane->SetRelativeScale3D(FVector(CardWidthCentimeters / 100.0f, CardHeightCentimeters / 100.0f, 1.0f));
}

UTexture2D* AOnokoArcanaCardActor::ResolveCurrentTexture() const
{
	if (bFaceUp && !CurrentCard.Texture.IsNull())
	{
		return CurrentCard.Texture.LoadSynchronous();
	}

	if (!BackTexture.IsNull())
	{
		return BackTexture.LoadSynchronous();
	}

	return nullptr;
}
