#include "OnokoArcanaDeckRuntime.h"

#include "Dom/JsonObject.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace
{
bool ReadStringField(const TSharedPtr<FJsonObject>& Object, const FString& FieldName, FString& OutValue, FString& OutError)
{
	if (!Object.IsValid() || !Object->TryGetStringField(FieldName, OutValue) || OutValue.IsEmpty())
	{
		OutError = FString::Printf(TEXT("Missing or empty string field: %s"), *FieldName);
		return false;
	}
	return true;
}

bool ReadStringArrayField(const TSharedPtr<FJsonObject>& Object, const FString& FieldName, TArray<FString>& OutValues, FString& OutError)
{
	const TArray<TSharedPtr<FJsonValue>>* Values = nullptr;
	if (!Object.IsValid() || !Object->TryGetArrayField(FieldName, Values) || Values == nullptr || Values->Num() == 0)
	{
		OutError = FString::Printf(TEXT("Missing or empty string array field: %s"), *FieldName);
		return false;
	}

	OutValues.Reset();
	for (const TSharedPtr<FJsonValue>& Value : *Values)
	{
		FString Text;
		if (!Value.IsValid() || !Value->TryGetString(Text) || Text.IsEmpty())
		{
			OutError = FString::Printf(TEXT("Invalid string item in field: %s"), *FieldName);
			return false;
		}
		OutValues.Add(Text);
	}
	return true;
}

bool ParseCard(const TSharedPtr<FJsonObject>& CardObject, FOnokoArcanaCardDefinition& OutCard, FString& OutError)
{
	FString TexturePath;
	if (!ReadStringField(CardObject, TEXT("id"), OutCard.Id, OutError) ||
		!ReadStringField(CardObject, TEXT("number"), OutCard.Number, OutError) ||
		!ReadStringField(CardObject, TEXT("slug"), OutCard.Slug, OutError) ||
		!ReadStringField(CardObject, TEXT("englishName"), OutCard.EnglishName, OutError) ||
		!ReadStringField(CardObject, TEXT("japaneseName"), OutCard.JapaneseName, OutError) ||
		!ReadStringArrayField(CardObject, TEXT("uprightKeywords"), OutCard.UprightKeywords, OutError) ||
		!ReadStringArrayField(CardObject, TEXT("reversedKeywords"), OutCard.ReversedKeywords, OutError) ||
		!ReadStringField(CardObject, TEXT("studyFocus"), OutCard.StudyFocus, OutError) ||
		!ReadStringField(CardObject, TEXT("qaStatus"), OutCard.QaStatus, OutError) ||
		!ReadStringField(CardObject, TEXT("unrealTexture"), TexturePath, OutError))
	{
		return false;
	}

	if (OutCard.QaStatus != TEXT("Adopted"))
	{
		OutError = FString::Printf(TEXT("Card is not Adopted: %s"), *OutCard.Id);
		return false;
	}

	OutCard.Texture = TSoftObjectPtr<UTexture2D>(FSoftObjectPath(TexturePath));
	return true;
}
}

bool UOnokoArcanaDeckRuntime::LoadMajorArcanaV5Manifest(FString& OutErrorMessage)
{
	FString ManifestPath = FPaths::Combine(FPaths::ProjectDir(), TEXT("../../data/major-arcana-v5-deck.json"));
	ManifestPath = FPaths::ConvertRelativePathToFull(ManifestPath);
	FPaths::NormalizeFilename(ManifestPath);
	return LoadFromManifestFile(ManifestPath, OutErrorMessage);
}

bool UOnokoArcanaDeckRuntime::LoadFromManifestFile(const FString& ManifestPath, FString& OutErrorMessage)
{
	FString JsonText;
	if (!FFileHelper::LoadFileToString(JsonText, *ManifestPath))
	{
		OutErrorMessage = FString::Printf(TEXT("Could not read deck manifest: %s"), *ManifestPath);
		return false;
	}

	TSharedPtr<FJsonObject> Root;
	const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonText);
	if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
	{
		OutErrorMessage = FString::Printf(TEXT("Invalid deck manifest JSON: %s"), *ManifestPath);
		return false;
	}

	FString Status;
	if (!ReadStringField(Root, TEXT("deckId"), DeckId, OutErrorMessage) ||
		!ReadStringField(Root, TEXT("version"), Version, OutErrorMessage) ||
		!ReadStringField(Root, TEXT("status"), Status, OutErrorMessage))
	{
		return false;
	}

	if (DeckId != TEXT("onoko-arcana-major-v5") || Status != TEXT("candidate"))
	{
		OutErrorMessage = FString::Printf(TEXT("Unexpected deck manifest identity: deckId=%s status=%s"), *DeckId, *Status);
		return false;
	}

	const TSharedPtr<FJsonObject>* BackObject = nullptr;
	if (!Root->TryGetObjectField(TEXT("back"), BackObject) || BackObject == nullptr || !BackObject->IsValid())
	{
		OutErrorMessage = TEXT("Missing back object");
		return false;
	}

	FString BackTexturePath;
	FString BackStatus;
	if (!ReadStringField(*BackObject, TEXT("unrealTexture"), BackTexturePath, OutErrorMessage) ||
		!ReadStringField(*BackObject, TEXT("qaStatus"), BackStatus, OutErrorMessage))
	{
		return false;
	}
	if (BackStatus != TEXT("Adopted"))
	{
		OutErrorMessage = FString::Printf(TEXT("Back is not Adopted: %s"), *BackStatus);
		return false;
	}
	BackTexture = TSoftObjectPtr<UTexture2D>(FSoftObjectPath(BackTexturePath));

	const TArray<TSharedPtr<FJsonValue>>* CardValues = nullptr;
	if (!Root->TryGetArrayField(TEXT("cards"), CardValues) || CardValues == nullptr || CardValues->Num() != 22)
	{
		OutErrorMessage = FString::Printf(TEXT("Expected 22 Major Arcana cards, got %d"), CardValues ? CardValues->Num() : 0);
		return false;
	}

	Cards.Reset();
	TSet<FString> SeenIds;
	for (const TSharedPtr<FJsonValue>& CardValue : *CardValues)
	{
		const TSharedPtr<FJsonObject> CardObject = CardValue.IsValid() ? CardValue->AsObject() : nullptr;
		FOnokoArcanaCardDefinition Card;
		if (!ParseCard(CardObject, Card, OutErrorMessage))
		{
			return false;
		}
		if (SeenIds.Contains(Card.Id))
		{
			OutErrorMessage = FString::Printf(TEXT("Duplicate card id: %s"), *Card.Id);
			return false;
		}
		SeenIds.Add(Card.Id);
		Cards.Add(Card);
	}

	ResetDrawState();
	OutErrorMessage.Reset();
	return true;
}

void UOnokoArcanaDeckRuntime::ResetDrawState(int32 Seed, bool bUseSeed)
{
	bUseRandomStream = bUseSeed;
	if (bUseSeed)
	{
		RandomStream.Initialize(Seed);
	}
	RebuildRemaining();
}

bool UOnokoArcanaDeckRuntime::DrawOne(FOnokoArcanaDrawResult& OutResult, bool bAllowReversed)
{
	OutResult = FOnokoArcanaDrawResult();
	if (RemainingIndices.Num() == 0 || Cards.Num() == 0)
	{
		return false;
	}

	const int32 PickSlot = bUseRandomStream
		? RandomStream.RandRange(0, RemainingIndices.Num() - 1)
		: FMath::RandRange(0, RemainingIndices.Num() - 1);
	const int32 CardIndex = RemainingIndices[PickSlot];
	RemainingIndices.RemoveAtSwap(PickSlot, 1, EAllowShrinking::No);

	const bool bReversed = bAllowReversed && (bUseRandomStream ? RandomStream.RandRange(0, 1) == 1 : FMath::RandBool());

	OutResult.bSuccess = true;
	OutResult.Card = Cards[CardIndex];
	OutResult.Orientation = bReversed ? EOnokoArcanaCardOrientation::Reversed : EOnokoArcanaCardOrientation::Upright;
	OutResult.ActiveKeywords = bReversed ? Cards[CardIndex].ReversedKeywords : Cards[CardIndex].UprightKeywords;
	return true;
}

int32 UOnokoArcanaDeckRuntime::GetRemainingCount() const
{
	return RemainingIndices.Num();
}

void UOnokoArcanaDeckRuntime::RebuildRemaining()
{
	RemainingIndices.Reset();
	for (int32 Index = 0; Index < Cards.Num(); ++Index)
	{
		RemainingIndices.Add(Index);
	}
}
