#include "OnokoArcanaReadingHistoryViewModel.h"

#include "OnokoArcanaReadingSaveLibrary.h"

bool UOnokoArcanaReadingHistoryViewModel::LoadFromSlot(const FString& SlotName, int32 UserIndex)
{
	UOnokoArcanaReadingSaveGame* LoadedSaveGame = nullptr;
	const bool bLoaded = UOnokoArcanaReadingSaveLibrary::LoadReadingsFromSlot(
		SlotName,
		UserIndex,
		LoadedSaveGame,
		LastErrorMessage);
	if (!bLoaded)
	{
		SaveGame = nullptr;
		SelectedIndex = INDEX_NONE;
		return false;
	}

	SetSaveGame(LoadedSaveGame);
	LastErrorMessage.Reset();
	return true;
}

void UOnokoArcanaReadingHistoryViewModel::SetSaveGame(UOnokoArcanaReadingSaveGame* InSaveGame)
{
	SaveGame = InSaveGame;
	SelectedIndex = HasHistory() ? 0 : INDEX_NONE;
	LastErrorMessage.Reset();
}

bool UOnokoArcanaReadingHistoryViewModel::SelectReading(int32 Index)
{
	if (!GetReadingPtr(Index))
	{
		LastErrorMessage = FString::Printf(TEXT("Reading index is out of range: %d"), Index);
		return false;
	}

	SelectedIndex = Index;
	LastErrorMessage.Reset();
	return true;
}

void UOnokoArcanaReadingHistoryViewModel::ClearSelection()
{
	SelectedIndex = INDEX_NONE;
	LastErrorMessage.Reset();
}

bool UOnokoArcanaReadingHistoryViewModel::HasHistory() const
{
	return SaveGame && SaveGame->Readings.Num() > 0;
}

int32 UOnokoArcanaReadingHistoryViewModel::GetReadingCount() const
{
	return SaveGame ? SaveGame->Readings.Num() : 0;
}

int32 UOnokoArcanaReadingHistoryViewModel::GetSelectedIndex() const
{
	return SelectedIndex;
}

FOnokoArcanaSavedReading UOnokoArcanaReadingHistoryViewModel::GetSelectedReading() const
{
	const FOnokoArcanaSavedReading* Reading = GetReadingPtr(SelectedIndex);
	return Reading ? *Reading : FOnokoArcanaSavedReading();
}

FString UOnokoArcanaReadingHistoryViewModel::GetEmptyStateText() const
{
	return HasHistory() ? FString() : TEXT("保存された占いはまだありません。");
}

FString UOnokoArcanaReadingHistoryViewModel::GetReadingSummary(int32 Index) const
{
	const FOnokoArcanaSavedReading* Reading = GetReadingPtr(Index);
	return Reading ? FormatReadingSummary(*Reading) : FString();
}

FString UOnokoArcanaReadingHistoryViewModel::GetLatestReadingSummary() const
{
	return GetReadingSummary(0);
}

FString UOnokoArcanaReadingHistoryViewModel::GetSelectedTitleText() const
{
	const FOnokoArcanaSavedReading* Reading = GetReadingPtr(SelectedIndex);
	if (!Reading)
	{
		return FString();
	}

	return FString::Printf(
		TEXT("%s %s / %s"),
		*Reading->CardNumber,
		*Reading->JapaneseName,
		*Reading->EnglishName);
}

FString UOnokoArcanaReadingHistoryViewModel::GetSelectedDetailText() const
{
	const FOnokoArcanaSavedReading* Reading = GetReadingPtr(SelectedIndex);
	return Reading ? FormatReadingDetail(*Reading) : FString();
}

const FOnokoArcanaSavedReading* UOnokoArcanaReadingHistoryViewModel::GetReadingPtr(int32 Index) const
{
	if (!SaveGame || !SaveGame->Readings.IsValidIndex(Index))
	{
		return nullptr;
	}
	return &SaveGame->Readings[Index];
}

FString UOnokoArcanaReadingHistoryViewModel::FormatReadingSummary(const FOnokoArcanaSavedReading& Reading)
{
	const FString QuestionText = Reading.Question.IsEmpty() ? TEXT("問いなし") : Reading.Question;
	const FString SpreadText = Reading.SpreadDisplayName.IsEmpty() ? TEXT("一枚引き") : Reading.SpreadDisplayName;
	return FString::Printf(
		TEXT("%s | %s | %s %s | %s"),
		*Reading.CreatedAtUtc.ToIso8601(),
		*SpreadText,
		*Reading.CardNumber,
		*Reading.JapaneseName,
		*QuestionText);
}

FString UOnokoArcanaReadingHistoryViewModel::FormatReadingDetail(const FOnokoArcanaSavedReading& Reading)
{
	const FString Keywords = FString::Join(Reading.ActiveKeywords, TEXT(" / "));
	const FString QuestionText = Reading.Question.IsEmpty() ? TEXT("問いなし") : Reading.Question;
	const FString NoteText = Reading.UserInterpretation.IsEmpty() ? TEXT("未記入") : Reading.UserInterpretation;
	const FString GuideText = Reading.bGuideRevealed ? Reading.StudyFocus : TEXT("ガイド未表示");
	const FString SpreadText = Reading.SpreadDisplayName.IsEmpty() ? TEXT("一枚引き") : Reading.SpreadDisplayName;
	const FString PositionText = Reading.PositionLabel.IsEmpty() ? TEXT("一枚引き") : Reading.PositionLabel;

	return FString::Printf(
		TEXT("日時: %s\n問い: %s\nスプレッド: %s (%d枚)\n位置: %s\nカード: %s %s / %s\n向き: %s\nキーワード: %s\n自分の解釈: %s\n学習ガイド: %s"),
		*Reading.CreatedAtUtc.ToIso8601(),
		*QuestionText,
		*SpreadText,
		Reading.CardCount,
		*PositionText,
		*Reading.CardNumber,
		*Reading.JapaneseName,
		*Reading.EnglishName,
		*Reading.OrientationLabel,
		*Keywords,
		*NoteText,
		*GuideText);
}
