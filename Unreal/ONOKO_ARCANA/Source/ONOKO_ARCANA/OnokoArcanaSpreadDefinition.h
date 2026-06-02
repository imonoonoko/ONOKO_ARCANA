#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OnokoArcanaSpreadDefinition.generated.h"

UENUM(BlueprintType)
enum class EOnokoArcanaSpreadLayoutType : uint8
{
	Single,
	Linear,
	Cross,
	Horseshoe,
	CelticCross,
	Relationship
};

USTRUCT(BlueprintType)
struct FOnokoArcanaSpreadSlotDefinition
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FName PositionKey;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FString DisplayLabel;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	int32 RevealOrder = 0;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FString GuidePrompt;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FVector TableLocationCm = FVector::ZeroVector;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	float TableYawDegrees = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	bool bDefaultSelected = false;
};

USTRUCT(BlueprintType)
struct FOnokoArcanaSpreadDefinition
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FName SpreadId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FString DisplayName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	FString Description;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	EOnokoArcanaSpreadLayoutType LayoutType = EOnokoArcanaSpreadLayoutType::Single;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TArray<FOnokoArcanaSpreadSlotDefinition> Slots;
};

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaSpreadRegistry : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Spread")
	TArray<FOnokoArcanaSpreadDefinition> Spreads;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Spread")
	void InitializeBuiltInSpreads();

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	int32 GetSpreadCount() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FName GetDefaultSpreadId() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	bool FindSpreadById(FName SpreadId, FOnokoArcanaSpreadDefinition& OutSpread) const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	TArray<FName> GetSpreadIds() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetSpreadListText() const;

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Spread")
	FString GetSpreadSlotListText(FName SpreadId) const;
};
