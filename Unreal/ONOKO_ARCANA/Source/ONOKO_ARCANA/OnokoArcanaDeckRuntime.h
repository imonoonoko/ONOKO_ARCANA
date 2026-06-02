#pragma once

#include "CoreMinimal.h"
#include "Engine/Texture2D.h"
#include "UObject/Object.h"
#include "OnokoArcanaDeckRuntime.generated.h"

UENUM(BlueprintType)
enum class EOnokoArcanaCardOrientation : uint8
{
	Upright,
	Reversed
};

USTRUCT(BlueprintType)
struct FOnokoArcanaCardDefinition
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString Id;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString Number;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString Slug;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString EnglishName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString JapaneseName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	TArray<FString> UprightKeywords;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	TArray<FString> ReversedKeywords;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString StudyFocus;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	FString QaStatus;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Card")
	TSoftObjectPtr<UTexture2D> Texture;
};

USTRUCT(BlueprintType)
struct FOnokoArcanaDrawResult
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Draw")
	bool bSuccess = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Draw")
	FOnokoArcanaCardDefinition Card;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Draw")
	EOnokoArcanaCardOrientation Orientation = EOnokoArcanaCardOrientation::Upright;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Draw")
	TArray<FString> ActiveKeywords;
};

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaDeckRuntime : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Deck")
	FString DeckId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Deck")
	FString Version;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Deck")
	TSoftObjectPtr<UTexture2D> BackTexture;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Deck")
	TArray<FOnokoArcanaCardDefinition> Cards;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Deck")
	bool LoadMajorArcanaV5Manifest(FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Deck")
	bool LoadFromManifestFile(const FString& ManifestPath, FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Deck")
	void ResetDrawState(int32 Seed = 0, bool bUseSeed = false);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Deck")
	bool DrawOne(FOnokoArcanaDrawResult& OutResult, bool bAllowReversed = true);

	UFUNCTION(BlueprintPure, Category = "ONOKO Arcana|Deck")
	int32 GetRemainingCount() const;

private:
	TArray<int32> RemainingIndices;
	FRandomStream RandomStream;
	bool bUseRandomStream = false;

	void RebuildRemaining();
};
