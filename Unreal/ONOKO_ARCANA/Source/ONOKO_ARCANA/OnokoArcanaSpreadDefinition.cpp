#include "OnokoArcanaSpreadDefinition.h"

namespace
{
FOnokoArcanaSpreadSlotDefinition MakeSlot(
	FName PositionKey,
	const FString& DisplayLabel,
	int32 RevealOrder,
	const FString& GuidePrompt,
	const FVector& TableLocationCm,
	float TableYawDegrees = 0.0f,
	bool bDefaultSelected = false)
{
	FOnokoArcanaSpreadSlotDefinition Slot;
	Slot.PositionKey = PositionKey;
	Slot.DisplayLabel = DisplayLabel;
	Slot.RevealOrder = RevealOrder;
	Slot.GuidePrompt = GuidePrompt;
	Slot.TableLocationCm = TableLocationCm;
	Slot.TableYawDegrees = TableYawDegrees;
	Slot.bDefaultSelected = bDefaultSelected;
	return Slot;
}

FOnokoArcanaSpreadDefinition MakeSpread(
	FName SpreadId,
	const FString& DisplayName,
	const FString& Description,
	EOnokoArcanaSpreadLayoutType LayoutType,
	TArray<FOnokoArcanaSpreadSlotDefinition>&& Slots)
{
	FOnokoArcanaSpreadDefinition Spread;
	Spread.SpreadId = SpreadId;
	Spread.DisplayName = DisplayName;
	Spread.Description = Description;
	Spread.LayoutType = LayoutType;
	Spread.Slots = MoveTemp(Slots);
	return Spread;
}
}

void UOnokoArcanaSpreadRegistry::InitializeBuiltInSpreads()
{
	Spreads.Reset();

	Spreads.Add(MakeSpread(
		TEXT("one_card"),
		TEXT("一枚引き"),
		TEXT("ひとつの問いに対して、今見るべき視点を一枚で読む。"),
		EOnokoArcanaSpreadLayoutType::Single,
		{
			MakeSlot(TEXT("present"), TEXT("一枚引き"), 1, TEXT("問い全体の焦点として読む。"), FVector(0.0f, 0.0f, 2.0f), 0.0f, true),
		}));

	Spreads.Add(MakeSpread(
		TEXT("three_card_past_present_future"),
		TEXT("過去・現在・未来"),
		TEXT("状況の流れを三段階で読み、変化の筋道を確認する。"),
		EOnokoArcanaSpreadLayoutType::Linear,
		{
			MakeSlot(TEXT("past"), TEXT("過去"), 1, TEXT("現在に影響している背景や前提を見る。"), FVector(0.0f, -120.0f, 2.0f)),
			MakeSlot(TEXT("present"), TEXT("現在"), 2, TEXT("今の中心課題や意識すべき状態を見る。"), FVector(0.0f, 0.0f, 2.0f), 0.0f, true),
			MakeSlot(TEXT("future"), TEXT("未来"), 3, TEXT("この流れの先に出やすい可能性を見る。"), FVector(0.0f, 120.0f, 2.0f)),
		}));

	Spreads.Add(MakeSpread(
		TEXT("five_card_cross"),
		TEXT("五枚クロス"),
		TEXT("中心課題、支え、障害、上位視点、根底を十字に読む。"),
		EOnokoArcanaSpreadLayoutType::Cross,
		{
			MakeSlot(TEXT("center"), TEXT("中心"), 1, TEXT("問いの中心にある主題を見る。"), FVector(0.0f, 0.0f, 2.0f), 0.0f, true),
			MakeSlot(TEXT("support"), TEXT("支え"), 2, TEXT("助けになる資質や味方を見る。"), FVector(0.0f, -120.0f, 2.0f)),
			MakeSlot(TEXT("challenge"), TEXT("障害"), 3, TEXT("妨げや誤解されやすい点を見る。"), FVector(0.0f, 120.0f, 2.0f)),
			MakeSlot(TEXT("higher_view"), TEXT("上位視点"), 4, TEXT("一段高い視点から意味を読む。"), FVector(120.0f, 0.0f, 2.0f)),
			MakeSlot(TEXT("root"), TEXT("根底"), 5, TEXT("根底にある動機や未整理の感情を見る。"), FVector(-120.0f, 0.0f, 2.0f)),
		}));

	Spreads.Add(MakeSpread(
		TEXT("seven_card_horseshoe"),
		TEXT("七枚ホースシュー"),
		TEXT("過去から助言までを弧状に並べ、流れと選択肢を読む。"),
		EOnokoArcanaSpreadLayoutType::Horseshoe,
		{
			MakeSlot(TEXT("past"), TEXT("過去"), 1, TEXT("この問いに至った過去の流れを見る。"), FVector(70.0f, -180.0f, 2.0f), -25.0f),
			MakeSlot(TEXT("present"), TEXT("現在"), 2, TEXT("現在の状況と課題を見る。"), FVector(120.0f, -90.0f, 2.0f), -10.0f),
			MakeSlot(TEXT("hidden_influence"), TEXT("隠れた影響"), 3, TEXT("見落としている影響や前提を見る。"), FVector(120.0f, 90.0f, 2.0f), 10.0f),
			MakeSlot(TEXT("obstacle"), TEXT("障害"), 4, TEXT("進行を妨げる要因を見る。"), FVector(70.0f, 180.0f, 2.0f), 25.0f),
			MakeSlot(TEXT("outside"), TEXT("周囲"), 5, TEXT("周囲の反応や環境を見る。"), FVector(-70.0f, 180.0f, 2.0f), -25.0f),
			MakeSlot(TEXT("action"), TEXT("行動"), 6, TEXT("次に取るべき行動の方向を見る。"), FVector(-120.0f, 90.0f, 2.0f), -10.0f),
			MakeSlot(TEXT("outcome"), TEXT("結果"), 7, TEXT("このまま進んだ時の着地点を見る。"), FVector(-120.0f, -90.0f, 2.0f), 10.0f, true),
		}));

	Spreads.Add(MakeSpread(
		TEXT("celtic_cross"),
		TEXT("ケルト十字"),
		TEXT("問題の核心、内外の影響、希望、結果までを広く読む十枚展開。"),
		EOnokoArcanaSpreadLayoutType::CelticCross,
		{
			MakeSlot(TEXT("present"), TEXT("現状"), 1, TEXT("問いの現在地を見る。"), FVector(0.0f, 0.0f, 2.0f), 0.0f, true),
			MakeSlot(TEXT("crossing"), TEXT("交差"), 2, TEXT("現状に交差する課題や力を見る。"), FVector(0.0f, 0.0f, 3.0f), 90.0f),
			MakeSlot(TEXT("root"), TEXT("根底"), 3, TEXT("根にある原因や無意識を見る。"), FVector(-120.0f, 0.0f, 2.0f)),
			MakeSlot(TEXT("past"), TEXT("過去"), 4, TEXT("過ぎた影響を見る。"), FVector(0.0f, -130.0f, 2.0f)),
			MakeSlot(TEXT("crown"), TEXT("意識"), 5, TEXT("表層の意識や目標を見る。"), FVector(120.0f, 0.0f, 2.0f)),
			MakeSlot(TEXT("near_future"), TEXT("近未来"), 6, TEXT("近い未来の展開を見る。"), FVector(0.0f, 130.0f, 2.0f)),
			MakeSlot(TEXT("self"), TEXT("自分"), 7, TEXT("自分自身の姿勢を見る。"), FVector(-160.0f, 260.0f, 2.0f)),
			MakeSlot(TEXT("environment"), TEXT("環境"), 8, TEXT("周囲や外部環境を見る。"), FVector(-50.0f, 260.0f, 2.0f)),
			MakeSlot(TEXT("hopes_fears"), TEXT("希望と不安"), 9, TEXT("期待と恐れの両面を見る。"), FVector(60.0f, 260.0f, 2.0f)),
			MakeSlot(TEXT("outcome"), TEXT("結果"), 10, TEXT("総合的な着地点を見る。"), FVector(170.0f, 260.0f, 2.0f)),
		}));

	Spreads.Add(MakeSpread(
		TEXT("relationship_line"),
		TEXT("関係性ライン"),
		TEXT("二者の状態、接点、課題、可能性を横並びに読む。"),
		EOnokoArcanaSpreadLayoutType::Relationship,
		{
			MakeSlot(TEXT("self"), TEXT("自分"), 1, TEXT("自分側の状態を見る。"), FVector(0.0f, -250.0f, 2.0f)),
			MakeSlot(TEXT("other"), TEXT("相手"), 2, TEXT("相手側の状態を見る。"), FVector(0.0f, -150.0f, 2.0f)),
			MakeSlot(TEXT("bridge"), TEXT("接点"), 3, TEXT("二者をつなぐものを見る。"), FVector(0.0f, -50.0f, 2.0f), 0.0f, true),
			MakeSlot(TEXT("challenge"), TEXT("課題"), 4, TEXT("関係性の課題を見る。"), FVector(0.0f, 50.0f, 2.0f)),
			MakeSlot(TEXT("advice"), TEXT("助言"), 5, TEXT("関係性を扱う助言を見る。"), FVector(0.0f, 150.0f, 2.0f)),
			MakeSlot(TEXT("potential"), TEXT("可能性"), 6, TEXT("関係性の可能性を見る。"), FVector(0.0f, 250.0f, 2.0f)),
		}));
}

int32 UOnokoArcanaSpreadRegistry::GetSpreadCount() const
{
	return Spreads.Num();
}

FName UOnokoArcanaSpreadRegistry::GetDefaultSpreadId() const
{
	return Spreads.Num() > 0 ? Spreads[0].SpreadId : FName(TEXT("one_card"));
}

bool UOnokoArcanaSpreadRegistry::FindSpreadById(FName SpreadId, FOnokoArcanaSpreadDefinition& OutSpread) const
{
	for (const FOnokoArcanaSpreadDefinition& Spread : Spreads)
	{
		if (Spread.SpreadId == SpreadId)
		{
			OutSpread = Spread;
			return true;
		}
	}

	OutSpread = FOnokoArcanaSpreadDefinition();
	return false;
}

TArray<FName> UOnokoArcanaSpreadRegistry::GetSpreadIds() const
{
	TArray<FName> SpreadIds;
	SpreadIds.Reserve(Spreads.Num());
	for (const FOnokoArcanaSpreadDefinition& Spread : Spreads)
	{
		SpreadIds.Add(Spread.SpreadId);
	}
	return SpreadIds;
}

FString UOnokoArcanaSpreadRegistry::GetSpreadListText() const
{
	TArray<FString> Lines;
	Lines.Reserve(Spreads.Num());
	for (const FOnokoArcanaSpreadDefinition& Spread : Spreads)
	{
		Lines.Add(FString::Printf(TEXT("%s: %s (%d枚)"), *Spread.SpreadId.ToString(), *Spread.DisplayName, Spread.Slots.Num()));
	}
	return FString::Join(Lines, TEXT("\n"));
}

FString UOnokoArcanaSpreadRegistry::GetSpreadSlotListText(FName SpreadId) const
{
	FOnokoArcanaSpreadDefinition Spread;
	if (!FindSpreadById(SpreadId, Spread))
	{
		return FString();
	}

	TArray<FString> Lines;
	Lines.Reserve(Spread.Slots.Num());
	for (const FOnokoArcanaSpreadSlotDefinition& Slot : Spread.Slots)
	{
		Lines.Add(FString::Printf(TEXT("%d. %s [%s]"), Slot.RevealOrder, *Slot.DisplayLabel, *Slot.PositionKey.ToString()));
	}
	return FString::Join(Lines, TEXT("\n"));
}
