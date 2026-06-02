#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "OnokoArcanaReadingSaveGame.generated.h"

USTRUCT(BlueprintType)
struct FOnokoArcanaSavedReadingCardState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString PositionKey;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString PositionLabel;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	int32 RevealOrder = 0;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString CardId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString CardNumber;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString EnglishName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString JapaneseName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString OrientationLabel;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	TArray<FString> ActiveKeywords;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString StudyFocus;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString UserInterpretation;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	bool bRevealed = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	bool bGuideRevealed = false;
};

USTRUCT(BlueprintType)
struct FOnokoArcanaSavedReading
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString ReadingId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FDateTime CreatedAtUtc;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString Question;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString SpreadId = TEXT("one_card");

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString SpreadDisplayName = TEXT("一枚引き");

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	int32 CardCount = 1;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString PositionKey = TEXT("present");

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString PositionLabel = TEXT("一枚引き");

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString CardId;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString CardNumber;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString EnglishName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString JapaneseName;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString OrientationLabel;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	TArray<FString> ActiveKeywords;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString StudyFocus;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	FString UserInterpretation;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	bool bGuideRevealed = false;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	TArray<FOnokoArcanaSavedReadingCardState> CardStates;
};

UCLASS(BlueprintType)
class ONOKO_ARCANA_API UOnokoArcanaReadingSaveGame : public USaveGame
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	int32 SchemaVersion = 2;

	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|Save")
	TArray<FOnokoArcanaSavedReading> Readings;
};
