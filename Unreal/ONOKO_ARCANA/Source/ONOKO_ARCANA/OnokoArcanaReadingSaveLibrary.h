#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OnokoArcanaReadingSaveGame.h"
#include "OnokoArcanaReadingSaveLibrary.generated.h"

class UOnokoArcanaOneCardSession;
class UOnokoArcanaSpreadReadingSession;

UCLASS()
class ONOKO_ARCANA_API UOnokoArcanaReadingSaveLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	static bool MakeSavedReadingFromSession(
		const UOnokoArcanaOneCardSession* Session,
		FOnokoArcanaSavedReading& OutReading,
		FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	static bool MakeSavedReadingFromSpreadSession(
		const UOnokoArcanaSpreadReadingSession* Session,
		FOnokoArcanaSavedReading& OutReading,
		FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	static bool SaveReadingToSlot(
		const FOnokoArcanaSavedReading& Reading,
		const FString& SlotName,
		int32 UserIndex,
		FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	static bool LoadReadingsFromSlot(
		const FString& SlotName,
		int32 UserIndex,
		UOnokoArcanaReadingSaveGame*& OutSaveGame,
		FString& OutErrorMessage);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|Save")
	static bool DeleteReadingsSlot(
		const FString& SlotName,
		int32 UserIndex);
};
