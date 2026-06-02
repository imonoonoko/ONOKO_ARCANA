#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "OnokoArcanaDeckRuntime.h"
#include "OnokoArcanaCardActor.generated.h"

class UMaterialInstanceDynamic;
class UMaterialInterface;
class USceneComponent;
class UStaticMeshComponent;
class UTexture2D;

UCLASS(BlueprintType)
class ONOKO_ARCANA_API AOnokoArcanaCardActor : public AActor
{
	GENERATED_BODY()

public:
	AOnokoArcanaCardActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	TObjectPtr<UStaticMeshComponent> CardPlane;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Card")
	TObjectPtr<UMaterialInterface> CardMaterialBase;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Card")
	TSoftObjectPtr<UTexture2D> BackTexture;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Card")
	FName CardTextureParameterName = TEXT("CardTexture");

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Card", meta = (ClampMin = "1.0"))
	float CardWidthCentimeters = 72.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ONOKO Arcana|Card", meta = (ClampMin = "1.0"))
	float CardHeightCentimeters = 108.0f;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FOnokoArcanaCardDefinition CurrentCard;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	EOnokoArcanaCardOrientation CurrentOrientation = EOnokoArcanaCardOrientation::Upright;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	bool bFaceUp = false;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	void ConfigureCardScale(float WidthCentimeters, float HeightCentimeters);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	bool SetBackTexture(TSoftObjectPtr<UTexture2D> InBackTexture);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	bool SetCard(const FOnokoArcanaCardDefinition& InCard, EOnokoArcanaCardOrientation InOrientation, bool bRevealImmediately);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	bool ShowBack();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	bool RevealFront();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Card")
	bool ApplyVisual();

private:
	UPROPERTY(Transient)
	TObjectPtr<UMaterialInstanceDynamic> DynamicCardMaterial;

	void ApplyCardScale();
	UTexture2D* ResolveCurrentTexture() const;
};
