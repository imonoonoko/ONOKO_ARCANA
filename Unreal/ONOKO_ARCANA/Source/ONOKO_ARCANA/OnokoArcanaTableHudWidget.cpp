#include "OnokoArcanaTableHudWidget.h"

#include "Blueprint/WidgetTree.h"
#include "Components/Border.h"
#include "Components/Button.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/ComboBoxString.h"
#include "Components/EditableTextBox.h"
#include "Components/HorizontalBox.h"
#include "Components/HorizontalBoxSlot.h"
#include "Components/Image.h"
#include "Components/MultiLineEditableTextBox.h"
#include "Components/ScrollBox.h"
#include "Components/SizeBox.h"
#include "Components/TextBlock.h"
#include "Components/VerticalBox.h"
#include "Components/VerticalBoxSlot.h"
#include "EngineUtils.h"
#include "OnokoArcanaTableController.h"
#include "OnokoArcanaOneCardViewModel.h"
#include "OnokoArcanaReadingHistoryViewModel.h"
#include "OnokoArcanaSpreadDefinition.h"
#include "OnokoArcanaSpreadReadingViewModel.h"
#include "Engine/Texture2D.h"

namespace
{
constexpr float OnokoPanelAlpha = 0.76f;
const FLinearColor OnokoBackdropColor(0.0f, 0.004f, 0.010f, 0.36f);
const FLinearColor OnokoPanelColor(0.010f, 0.020f, 0.034f, OnokoPanelAlpha);
const FLinearColor OnokoPanelLayerColor(0.024f, 0.044f, 0.070f, 0.84f);
const FLinearColor OnokoInkColor(0.86f, 0.94f, 1.0f, 1.0f);
const FLinearColor OnokoMutedInkColor(0.58f, 0.70f, 0.80f, 1.0f);
const FLinearColor OnokoGoldColor(0.86f, 0.70f, 0.38f, 1.0f);
const FLinearColor OnokoBlueColor(0.22f, 0.62f, 1.0f, 1.0f);
const FLinearColor OnokoBlueDimColor(0.04f, 0.16f, 0.28f, 0.82f);

void SetCanvasSlot(UWidget* Widget, const FAnchors& Anchors, const FMargin& Offsets, int32 ZOrder)
{
	if (UCanvasPanelSlot* CanvasSlot = Widget ? Cast<UCanvasPanelSlot>(Widget->Slot) : nullptr)
	{
		CanvasSlot->SetAnchors(Anchors);
		CanvasSlot->SetOffsets(Offsets);
		CanvasSlot->SetZOrder(ZOrder);
	}
}

void SetFixedCanvasSlot(UWidget* Widget, const FVector2D& Position, const FVector2D& Size, int32 ZOrder)
{
	if (UCanvasPanelSlot* CanvasSlot = Widget ? Cast<UCanvasPanelSlot>(Widget->Slot) : nullptr)
	{
		CanvasSlot->SetAnchors(FAnchors(0.0f, 0.0f, 0.0f, 0.0f));
		CanvasSlot->SetAlignment(FVector2D(0.0f, 0.0f));
		CanvasSlot->SetPosition(Position);
		CanvasSlot->SetSize(Size);
		CanvasSlot->SetZOrder(ZOrder);
	}
}
}

void UOnokoArcanaTableHudWidget::NativeOnInitialized()
{
	Super::NativeOnInitialized();

	BuildNativeFallbackWidgetTreeIfNeeded();

	if (StartReadingButton)
	{
		StartReadingButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleStartReadingClicked);
	}
	if (DrawButton)
	{
		DrawButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleDrawClicked);
	}
	if (RevealCardButton)
	{
		RevealCardButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleRevealCardClicked);
	}
	if (RevealGuideButton)
	{
		RevealGuideButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleRevealGuideClicked);
	}
	if (ResetButton)
	{
		ResetButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleResetClicked);
	}
	if (SaveReadingButton)
	{
		SaveReadingButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleSaveReadingClicked);
	}
	if (RefreshHistoryButton)
	{
		RefreshHistoryButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleRefreshHistoryClicked);
	}
	if (SpreadSelectorComboBox)
	{
		SpreadSelectorComboBox->OnSelectionChanged.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleSpreadSelectionChanged);
	}
	if (PastSlotButton)
	{
		PastSlotButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandlePastSlotClicked);
	}
	if (PresentSlotButton)
	{
		PresentSlotButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandlePresentSlotClicked);
	}
	if (FutureSlotButton)
	{
		FutureSlotButton->OnClicked.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleFutureSlotClicked);
	}
	if (UserInterpretationTextBox)
	{
		UserInterpretationTextBox->OnTextChanged.AddDynamic(this, &UOnokoArcanaTableHudWidget::HandleUserInterpretationChanged);
	}

	FindTableControllerInWorld();
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SetTableController(AOnokoArcanaTableController* InTableController)
{
	TableController = InTableController;
	RefreshSpreadSelectorOptions();
	RefreshFromController();
}

bool UOnokoArcanaTableHudWidget::FindTableControllerInWorld()
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

void UOnokoArcanaTableHudWidget::RefreshFromController()
{
	if (!TableController)
	{
		FindTableControllerInWorld();
	}

	if (!TableController)
	{
		SetTextIfBound(StateText, TEXT("テーブル未接続"));
		SetTextIfBound(ErrorText, TEXT("AOnokoArcanaTableController が見つかりません。"));
		SetEnabledIfBound(DrawButton, false);
		SetEnabledIfBound(RevealCardButton, false);
		SetEnabledIfBound(RevealGuideButton, false);
		SetEnabledIfBound(ResetButton, false);
		SetEnabledIfBound(SaveReadingButton, false);
		SetEnabledIfBound(RefreshHistoryButton, false);
		SetEnabledIfBound(SpreadSelectorComboBox, false);
		SetEnabledIfBound(PastSlotButton, false);
		SetEnabledIfBound(PresentSlotButton, false);
		SetEnabledIfBound(FutureSlotButton, false);
		return;
	}

	if (!TableController->SpreadRegistry)
	{
		TableController->InitializeSpreadRegistry();
	}
	RefreshSpreadSelectorOptions();

	UOnokoArcanaOneCardViewModel* ViewModel = TableController->ViewModel;
	UOnokoArcanaSpreadReadingViewModel* SpreadViewModel = TableController->SpreadViewModel;
	UOnokoArcanaReadingHistoryViewModel* HistoryViewModel = TableController->HistoryViewModel;
	const bool bHasDraw = TableController->HasCurrentDraw();
	const bool bIsOneCard = TableController->IsOneCardSpread();
	const bool bCanDraw = bIsOneCard ? (ViewModel ? ViewModel->CanDraw() : true) : !bHasDraw;
	const bool bCanRevealCard = bIsOneCard ? bHasDraw : (SpreadViewModel && SpreadViewModel->CanRevealNext());
	const bool bCanRevealGuide = bIsOneCard ? (ViewModel ? ViewModel->CanRevealGuide() : bHasDraw) : (SpreadViewModel && SpreadViewModel->CanRevealSelectedGuide());
	const bool bCanSelectSpreadSlot = !bIsOneCard && TableController->IsSpreadReadingActive();
	const int32 HistoryCount = HistoryViewModel ? HistoryViewModel->GetReadingCount() : 0;

	SetTextIfBound(StateText, bIsOneCard ? (bHasDraw ? TEXT("カード選択済み") : TEXT("待機中")) : (SpreadViewModel ? SpreadViewModel->GetProgressText() : TEXT("スプレッド待機中")));
	SetTextIfBound(ErrorText, TableController->LastErrorMessage);
	SetTextIfBound(ActiveSpreadText, TableController->GetActiveSpreadDisplayText());
	SetTextIfBound(SpreadSlotsText, TableController->GetActiveSpreadSlotListText());
	SetTextIfBound(SelectedSpreadSlotText, TableController->GetSelectedSpreadSlotText());
	SetTextIfBound(CardTitleText, bIsOneCard ? (ViewModel ? ViewModel->GetCardTitle() : FString()) : (SpreadViewModel ? SpreadViewModel->GetSelectedCardTitle() : FString()));
	SetTextIfBound(OrientationText, bIsOneCard ? (ViewModel ? ViewModel->GetOrientationLabel() : FString()) : (SpreadViewModel ? SpreadViewModel->GetSelectedOrientationLabel() : FString()));
	SetTextIfBound(KeywordsText, bIsOneCard ? (ViewModel ? ViewModel->GetActiveKeywordsText() : FString()) : (SpreadViewModel ? SpreadViewModel->GetSelectedKeywordsText() : FString()));
	SetTextIfBound(StudyFocusText, bIsOneCard ? (ViewModel ? ViewModel->GetStudyFocusText() : FString()) : (SpreadViewModel ? SpreadViewModel->GetSelectedGuideText() : FString()));
	SetTextIfBound(HistoryCountText, FString::Printf(TEXT("保存履歴: %d件"), HistoryCount));
	SetTextIfBound(HistoryLatestSummaryText, HistoryViewModel ? HistoryViewModel->GetLatestReadingSummary() : FString());
	SetTextIfBound(HistorySelectedTitleText, HistoryViewModel ? HistoryViewModel->GetSelectedTitleText() : FString());
	SetTextIfBound(HistorySelectedDetailText, HistoryViewModel ? HistoryViewModel->GetSelectedDetailText() : FString());
	SetTextIfBound(HistoryEmptyStateText, HistoryViewModel ? HistoryViewModel->GetEmptyStateText() : TEXT("履歴未読込"));

	SetEnabledIfBound(StartReadingButton, true);
	SetEnabledIfBound(DrawButton, bCanDraw);
	SetEnabledIfBound(RevealCardButton, bCanRevealCard);
	SetEnabledIfBound(RevealGuideButton, bCanRevealGuide);
	SetEnabledIfBound(ResetButton, true);
	SetEnabledIfBound(SaveReadingButton, bHasDraw);
	SetEnabledIfBound(RefreshHistoryButton, true);
	SetEnabledIfBound(SpreadSelectorComboBox, !bHasDraw);
	SetEnabledIfBound(PastSlotButton, bCanSelectSpreadSlot);
	SetEnabledIfBound(PresentSlotButton, bCanSelectSpreadSlot);
	SetEnabledIfBound(FutureSlotButton, bCanSelectSpreadSlot);
}

void UOnokoArcanaTableHudWidget::StartReadingFromQuestion()
{
	if (!TableController)
	{
		FindTableControllerInWorld();
	}
	if (!TableController)
	{
		RefreshFromController();
		return;
	}

	TableController->StartReading(GetQuestionText());
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::DrawCard()
{
	if (!TableController)
	{
		FindTableControllerInWorld();
	}
	if (!TableController)
	{
		RefreshFromController();
		return;
	}

	TableController->DrawCard(false);
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::RevealCard()
{
	if (TableController)
	{
		TableController->RevealCard();
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::RevealGuide()
{
	if (TableController)
	{
		TableController->RevealGuide();
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::ResetTable()
{
	if (TableController)
	{
		TableController->ResetTable();
	}
	if (UserInterpretationTextBox)
	{
		UserInterpretationTextBox->SetText(FText::GetEmpty());
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SaveCurrentReading()
{
	if (TableController)
	{
		TableController->SaveCurrentReading();
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::RefreshReadingHistory()
{
	if (TableController)
	{
		TableController->RefreshReadingHistory();
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SelectHistoryReading(int32 Index)
{
	if (TableController)
	{
		TableController->SelectHistoryReading(Index);
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SelectSpreadById(FName SpreadId)
{
	if (!TableController)
	{
		FindTableControllerInWorld();
	}
	if (TableController)
	{
		TableController->SelectSpread(SpreadId);
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SelectSpreadSlotById(FName PositionKey)
{
	if (!TableController)
	{
		FindTableControllerInWorld();
	}
	if (TableController)
	{
		TableController->SelectSpreadSlot(PositionKey);
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::SubmitUserInterpretationText(const FText& Text)
{
	if (TableController)
	{
		TableController->SubmitUserInterpretation(Text.ToString());
	}
	RefreshFromController();
}

void UOnokoArcanaTableHudWidget::HandleStartReadingClicked()
{
	StartReadingFromQuestion();
}

void UOnokoArcanaTableHudWidget::HandleDrawClicked()
{
	DrawCard();
}

void UOnokoArcanaTableHudWidget::HandleRevealCardClicked()
{
	RevealCard();
}

void UOnokoArcanaTableHudWidget::HandleRevealGuideClicked()
{
	RevealGuide();
}

void UOnokoArcanaTableHudWidget::HandleResetClicked()
{
	ResetTable();
}

void UOnokoArcanaTableHudWidget::HandleSaveReadingClicked()
{
	SaveCurrentReading();
}

void UOnokoArcanaTableHudWidget::HandleRefreshHistoryClicked()
{
	RefreshReadingHistory();
}

void UOnokoArcanaTableHudWidget::HandleUserInterpretationChanged(const FText& Text)
{
	SubmitUserInterpretationText(Text);
}

void UOnokoArcanaTableHudWidget::HandleSpreadSelectionChanged(FString SelectedItem, ESelectInfo::Type SelectionType)
{
	if (SelectionType == ESelectInfo::Direct)
	{
		return;
	}

	SelectSpreadById(ExtractSpreadIdFromOption(SelectedItem));
}

void UOnokoArcanaTableHudWidget::HandlePastSlotClicked()
{
	SelectSpreadSlotById(FName(TEXT("past")));
}

void UOnokoArcanaTableHudWidget::HandlePresentSlotClicked()
{
	SelectSpreadSlotById(FName(TEXT("present")));
}

void UOnokoArcanaTableHudWidget::HandleFutureSlotClicked()
{
	SelectSpreadSlotById(FName(TEXT("future")));
}

void UOnokoArcanaTableHudWidget::SetTextIfBound(UTextBlock* TextBlock, const FString& Text)
{
	if (TextBlock)
	{
		TextBlock->SetText(FText::FromString(Text));
	}
}

void UOnokoArcanaTableHudWidget::SetEnabledIfBound(UWidget* Widget, bool bEnabled)
{
	if (Widget)
	{
		Widget->SetIsEnabled(bEnabled);
	}
}

FString UOnokoArcanaTableHudWidget::GetQuestionText() const
{
	if (QuestionTextBox)
	{
		return QuestionTextBox->GetText().ToString();
	}
	return FString();
}

void UOnokoArcanaTableHudWidget::RefreshSpreadSelectorOptions()
{
	if (!SpreadSelectorComboBox || !TableController)
	{
		return;
	}

	if (!TableController->SpreadRegistry)
	{
		TableController->InitializeSpreadRegistry();
	}
	const TArray<FOnokoArcanaSpreadDefinition> Spreads = TableController->GetAvailableSpreads();
	SpreadSelectorComboBox->ClearOptions();
	for (const FOnokoArcanaSpreadDefinition& Spread : Spreads)
	{
		SpreadSelectorComboBox->AddOption(MakeSpreadOptionLabel(Spread.SpreadId, Spread.DisplayName, Spread.Slots.Num()));
	}

	const FString ActiveIdString = TableController->ActiveSpreadId.ToString();
	for (int32 Index = 0; Index < SpreadSelectorComboBox->GetOptionCount(); ++Index)
	{
		const FString Option = SpreadSelectorComboBox->GetOptionAtIndex(Index);
		if (ExtractSpreadIdFromOption(Option).ToString() == ActiveIdString)
		{
			SpreadSelectorComboBox->SetSelectedOption(Option);
			break;
		}
	}
}

FString UOnokoArcanaTableHudWidget::MakeSpreadOptionLabel(FName SpreadId, const FString& DisplayName, int32 CardCount)
{
	return FString::Printf(TEXT("%s - %s (%d)"), *SpreadId.ToString(), *DisplayName, CardCount);
}

FName UOnokoArcanaTableHudWidget::ExtractSpreadIdFromOption(const FString& OptionLabel)
{
	FString Left;
	FString Right;
	if (OptionLabel.Split(TEXT(" - "), &Left, &Right))
	{
		return FName(*Left);
	}
	return FName(*OptionLabel);
}

void UOnokoArcanaTableHudWidget::BuildNativeFallbackWidgetTreeIfNeeded()
{
	if (!WidgetTree || WidgetTree->RootWidget)
	{
		return;
	}

	UCanvasPanel* RootPanel = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("NativeFallbackRoot"));
	WidgetTree->RootWidget = RootPanel;

	UBorder* Backdrop = CreateNativePanel(TEXT("NativeFallbackBackdrop"), FMargin(0.0f), OnokoBackdropColor);
	RootPanel->AddChild(Backdrop);
	SetCanvasSlot(Backdrop, FAnchors(0.0f, 0.0f, 1.0f, 1.0f), FMargin(0.0f), 0);

	if (UTexture2D* HudOverlayTexture = LoadObject<UTexture2D>(
		nullptr,
		TEXT("/Game/ONOKOArcana/UI/HUD/Textures/T_HUD_ONOKO_Overlay_V1.T_HUD_ONOKO_Overlay_V1")))
	{
		UImage* HudOverlayImage = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), TEXT("NativeFallbackHudGeneratedOverlay"));
		HudOverlayImage->SetBrushFromTexture(HudOverlayTexture, false);
		HudOverlayImage->SetColorAndOpacity(FLinearColor(1.0f, 1.0f, 1.0f, 0.92f));
		RootPanel->AddChild(HudOverlayImage);
		SetCanvasSlot(HudOverlayImage, FAnchors(0.0f, 0.0f, 1.0f, 1.0f), FMargin(0.0f), 1);
	}

	UBorder* TopNameplate = CreateNativePanel(TEXT("NativeFallbackTopNameplate"), FMargin(10.0f, 4.0f), FLinearColor(0.0f, 0.0f, 0.0f, 0.0f));
	RootPanel->AddChild(TopNameplate);
	SetFixedCanvasSlot(TopNameplate, FVector2D(740.0f, 80.0f), FVector2D(360.0f, 36.0f), 3);
	UVerticalBox* TopNameplateBox = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(), TEXT("NativeFallbackTopNameplateBox"));
	TopNameplate->SetContent(TopNameplateBox);
	UTextBlock* TopTitleText = CreateNativeTextBlock(TEXT("NativeFallbackTopTitleText"), TEXT("ONOKO ARCANA"), 22);
	TopTitleText->SetJustification(ETextJustify::Center);
	TopTitleText->SetColorAndOpacity(FSlateColor(OnokoInkColor));
	AddNativeRow(TopNameplateBox, TopTitleText, FMargin(0.0f));

	UBorder* LeftPanel = CreateNativePanel(TEXT("NativeFallbackLeftPanel"), FMargin(18.0f), OnokoPanelColor);
	RootPanel->AddChild(LeftPanel);
	SetFixedCanvasSlot(LeftPanel, FVector2D(42.0f, 104.0f), FVector2D(296.0f, 714.0f), 2);

	UScrollBox* ScrollBox = WidgetTree->ConstructWidget<UScrollBox>(UScrollBox::StaticClass(), TEXT("NativeFallbackLeftScroll"));
	LeftPanel->SetContent(ScrollBox);

	UVerticalBox* MainBox = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(), TEXT("NativeFallbackMainBox"));
	ScrollBox->AddChild(MainBox);

	UTextBlock* TitleText = CreateNativeTextBlock(TEXT("NativeFallbackTitleText"), TEXT("READING SETUP"), 14);
	TitleText->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	AddNativeRow(MainBox, TitleText, FMargin(0.0f, 0.0f, 0.0f, 12.0f));

	AddNativeRow(MainBox, CreateNativeSectionTitle(TEXT("NativeFallbackSpreadLabel"), TEXT("スプレッド")), FMargin(0.0f, 0.0f, 0.0f, 4.0f));
	SpreadSelectorComboBox = WidgetTree->ConstructWidget<UComboBoxString>(UComboBoxString::StaticClass(), TEXT("SpreadSelectorComboBox"));
	AddNativeRow(MainBox, SpreadSelectorComboBox);

	ActiveSpreadText = CreateNativeTextBlock(TEXT("ActiveSpreadText"), FString(), 15);
	ActiveSpreadText->SetColorAndOpacity(FSlateColor(OnokoInkColor));
	AddNativeRow(MainBox, ActiveSpreadText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));

	SpreadSlotsText = CreateNativeTextBlock(TEXT("SpreadSlotsText"), FString(), 12);
	SpreadSlotsText->SetColorAndOpacity(FSlateColor(OnokoMutedInkColor));
	AddNativeRow(MainBox, SpreadSlotsText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));

	SelectedSpreadSlotText = CreateNativeTextBlock(TEXT("SelectedSpreadSlotText"), FString(), 13);
	SelectedSpreadSlotText->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	AddNativeRow(MainBox, SelectedSpreadSlotText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));

	AddNativeRow(MainBox, CreateNativeSectionTitle(TEXT("NativeFallbackQuestionLabel"), TEXT("問い")), FMargin(0.0f, 8.0f, 0.0f, 4.0f));
	QuestionTextBox = WidgetTree->ConstructWidget<UEditableTextBox>(UEditableTextBox::StaticClass(), TEXT("QuestionTextBox"));
	QuestionTextBox->SetHintText(FText::FromString(TEXT("今の自分に必要な視点は？")));
	QuestionTextBox->SetForegroundColor(OnokoInkColor);
	FEditableTextBoxStyle QuestionTextBoxStyle = QuestionTextBox->GetWidgetStyle();
	QuestionTextBoxStyle.SetForegroundColor(FSlateColor(OnokoInkColor));
	QuestionTextBoxStyle.SetFocusedForegroundColor(FSlateColor(OnokoInkColor));
	QuestionTextBoxStyle.SetBackgroundColor(FSlateColor(OnokoPanelLayerColor));
	QuestionTextBoxStyle.BackgroundImageNormal.TintColor = FSlateColor(OnokoPanelLayerColor);
	QuestionTextBoxStyle.BackgroundImageHovered.TintColor = FSlateColor(FLinearColor(0.035f, 0.078f, 0.120f, 0.94f));
	QuestionTextBoxStyle.BackgroundImageFocused.TintColor = FSlateColor(FLinearColor(0.030f, 0.094f, 0.150f, 0.96f));
	QuestionTextBoxStyle.BackgroundImageReadOnly.TintColor = FSlateColor(OnokoPanelLayerColor);
	QuestionTextBox->SetWidgetStyle(QuestionTextBoxStyle);
	AddNativeRow(MainBox, QuestionTextBox);

	AddNativeRow(MainBox, CreateNativeSectionTitle(TEXT("NativeFallbackInterpretationLabel"), TEXT("自分の解釈")), FMargin(0.0f, 10.0f, 0.0f, 4.0f));
	UserInterpretationTextBox = WidgetTree->ConstructWidget<UMultiLineEditableTextBox>(
		UMultiLineEditableTextBox::StaticClass(),
		TEXT("UserInterpretationTextBox"));
	UserInterpretationTextBox->SetHintText(FText::FromString(TEXT("カードを見て、先に自分の言葉で読んだ内容を書く。")));
	UserInterpretationTextBox->SetForegroundColor(OnokoInkColor);
	UserInterpretationTextBox->WidgetStyle.SetForegroundColor(FSlateColor(OnokoInkColor));
	UserInterpretationTextBox->WidgetStyle.SetFocusedForegroundColor(FSlateColor(OnokoInkColor));
	UserInterpretationTextBox->WidgetStyle.SetBackgroundColor(FSlateColor(OnokoPanelLayerColor));
	UserInterpretationTextBox->WidgetStyle.BackgroundImageNormal.TintColor = FSlateColor(OnokoPanelLayerColor);
	UserInterpretationTextBox->WidgetStyle.BackgroundImageHovered.TintColor = FSlateColor(FLinearColor(0.035f, 0.078f, 0.120f, 0.94f));
	UserInterpretationTextBox->WidgetStyle.BackgroundImageFocused.TintColor = FSlateColor(FLinearColor(0.030f, 0.094f, 0.150f, 0.96f));
	UserInterpretationTextBox->WidgetStyle.BackgroundImageReadOnly.TintColor = FSlateColor(OnokoPanelLayerColor);
	if (USizeBox* InterpretationSizeBox = WidgetTree->ConstructWidget<USizeBox>(USizeBox::StaticClass(), TEXT("NativeFallbackInterpretationSizeBox")))
	{
		InterpretationSizeBox->SetMinDesiredHeight(150.0f);
		InterpretationSizeBox->SetContent(UserInterpretationTextBox);
		AddNativeRow(MainBox, InterpretationSizeBox);
	}

	StateText = CreateNativeTextBlock(TEXT("StateText"), TEXT("待機中"), 15);
	StateText->SetColorAndOpacity(FSlateColor(OnokoInkColor));
	AddNativeRow(MainBox, StateText, FMargin(0.0f, 4.0f, 0.0f, 4.0f));

	ErrorText = CreateNativeTextBlock(TEXT("ErrorText"), FString(), 14);
	ErrorText->SetColorAndOpacity(FSlateColor(FLinearColor(1.0f, 0.56f, 0.48f, 1.0f)));
	AddNativeRow(MainBox, ErrorText);

	UBorder* RightPanel = CreateNativePanel(TEXT("NativeFallbackRightPanel"), FMargin(18.0f), OnokoPanelColor);
	RootPanel->AddChild(RightPanel);
	SetFixedCanvasSlot(RightPanel, FVector2D(1510.0f, 116.0f), FVector2D(350.0f, 840.0f), 2);

	UScrollBox* RightScrollBox = WidgetTree->ConstructWidget<UScrollBox>(UScrollBox::StaticClass(), TEXT("NativeFallbackRightScroll"));
	RightPanel->SetContent(RightScrollBox);
	UVerticalBox* RightBox = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass(), TEXT("NativeFallbackRightBox"));
	RightScrollBox->AddChild(RightBox);

	AddNativeRow(RightBox, CreateNativeSectionTitle(TEXT("NativeFallbackGuideLabel"), TEXT("選択中のカードガイド")), FMargin(0.0f, 0.0f, 0.0f, 8.0f));

	CardTitleText = CreateNativeTextBlock(TEXT("CardTitleText"), FString(), 20);
	CardTitleText->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	AddNativeRow(RightBox, CardTitleText, FMargin(0.0f, 2.0f, 0.0f, 6.0f));

	OrientationText = CreateNativeTextBlock(TEXT("OrientationText"), FString(), 15);
	OrientationText->SetColorAndOpacity(FSlateColor(OnokoInkColor));
	AddNativeRow(RightBox, OrientationText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));

	KeywordsText = CreateNativeTextBlock(TEXT("KeywordsText"), FString(), 15);
	KeywordsText->SetColorAndOpacity(FSlateColor(OnokoMutedInkColor));
	AddNativeRow(RightBox, KeywordsText, FMargin(0.0f, 0.0f, 0.0f, 10.0f));

	StudyFocusText = CreateNativeTextBlock(TEXT("StudyFocusText"), FString(), 15);
	StudyFocusText->SetColorAndOpacity(FSlateColor(FLinearColor(0.74f, 0.90f, 1.0f, 1.0f)));
	AddNativeRow(RightBox, StudyFocusText, FMargin(0.0f, 0.0f, 0.0f, 16.0f));

	AddNativeRow(RightBox, CreateNativeSectionTitle(TEXT("NativeFallbackHistoryLabel"), TEXT("リーディング履歴")), FMargin(0.0f, 8.0f, 0.0f, 8.0f));
	HistoryCountText = CreateNativeTextBlock(TEXT("HistoryCountText"), TEXT("保存履歴: 0件"), 14);
	HistoryLatestSummaryText = CreateNativeTextBlock(TEXT("HistoryLatestSummaryText"), FString(), 13);
	HistorySelectedTitleText = CreateNativeTextBlock(TEXT("HistorySelectedTitleText"), FString(), 14);
	HistorySelectedTitleText->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	HistorySelectedDetailText = CreateNativeTextBlock(TEXT("HistorySelectedDetailText"), FString(), 13);
	HistoryEmptyStateText = CreateNativeTextBlock(TEXT("HistoryEmptyStateText"), TEXT("履歴未読込"), 13);
	HistoryEmptyStateText->SetColorAndOpacity(FSlateColor(OnokoMutedInkColor));
	AddNativeRow(RightBox, HistoryCountText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));
	AddNativeRow(RightBox, HistoryLatestSummaryText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));
	AddNativeRow(RightBox, HistorySelectedTitleText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));
	AddNativeRow(RightBox, HistorySelectedDetailText, FMargin(0.0f, 0.0f, 0.0f, 4.0f));
	AddNativeRow(RightBox, HistoryEmptyStateText, FMargin(0.0f));

	UBorder* BottomPanel = CreateNativePanel(TEXT("NativeFallbackBottomCommandBar"), FMargin(12.0f, 10.0f), OnokoPanelColor);
	RootPanel->AddChild(BottomPanel);
	SetFixedCanvasSlot(BottomPanel, FVector2D(500.0f, 960.0f), FVector2D(960.0f, 62.0f), 3);

	UHorizontalBox* CommandRow = WidgetTree->ConstructWidget<UHorizontalBox>(UHorizontalBox::StaticClass(), TEXT("NativeFallbackCommandRow"));
	BottomPanel->SetContent(CommandRow);

	PastSlotButton = CreateNativeButton(TEXT("PastSlotButton"), TEXT("Past"));
	PresentSlotButton = CreateNativeButton(TEXT("PresentSlotButton"), TEXT("Present"));
	FutureSlotButton = CreateNativeButton(TEXT("FutureSlotButton"), TEXT("Future"));
	StartReadingButton = CreateNativeButton(TEXT("StartReadingButton"), TEXT("Start"));
	DrawButton = CreateNativeButton(TEXT("DrawButton"), TEXT("Draw"));
	RevealCardButton = CreateNativeButton(TEXT("RevealCardButton"), TEXT("Reveal"));
	RevealGuideButton = CreateNativeButton(TEXT("RevealGuideButton"), TEXT("Guide"));
	SaveReadingButton = CreateNativeButton(TEXT("SaveReadingButton"), TEXT("Save"));
	RefreshHistoryButton = CreateNativeButton(TEXT("RefreshHistoryButton"), TEXT("History"));
	ResetButton = CreateNativeButton(TEXT("ResetButton"), TEXT("Reset"));
	for (UButton* Button : {PastSlotButton.Get(), PresentSlotButton.Get(), FutureSlotButton.Get(), StartReadingButton.Get(), DrawButton.Get(), RevealCardButton.Get(), RevealGuideButton.Get(), SaveReadingButton.Get(), RefreshHistoryButton.Get(), ResetButton.Get()})
	{
		AddNativeButtonToRow(CommandRow, Button);
	}
}

UBorder* UOnokoArcanaTableHudWidget::CreateNativePanel(FName WidgetName, const FMargin& PanelPadding, const FLinearColor& BrushColor)
{
	UBorder* Panel = WidgetTree->ConstructWidget<UBorder>(UBorder::StaticClass(), WidgetName);
	Panel->SetPadding(PanelPadding);
	Panel->SetBrushColor(BrushColor);
	return Panel;
}

UTextBlock* UOnokoArcanaTableHudWidget::CreateNativeTextBlock(FName WidgetName, const FString& Text, int32 FontSize)
{
	UTextBlock* TextBlock = WidgetTree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), WidgetName);
	TextBlock->SetText(FText::FromString(Text));
	TextBlock->SetAutoWrapText(true);
	TextBlock->SetColorAndOpacity(FSlateColor(OnokoInkColor));
	TextBlock->SetShadowColorAndOpacity(FLinearColor(0.0f, 0.28f, 0.58f, 0.45f));
	TextBlock->SetShadowOffset(FVector2D(0.0f, 1.0f));

	FSlateFontInfo FontInfo = TextBlock->GetFont();
	FontInfo.Size = FontSize;
	TextBlock->SetFont(FontInfo);
	return TextBlock;
}

UTextBlock* UOnokoArcanaTableHudWidget::CreateNativeSectionTitle(FName WidgetName, const FString& Text)
{
	UTextBlock* TextBlock = CreateNativeTextBlock(WidgetName, Text, 13);
	TextBlock->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	return TextBlock;
}

UButton* UOnokoArcanaTableHudWidget::CreateNativeButton(FName WidgetName, const FString& Label)
{
	UButton* Button = WidgetTree->ConstructWidget<UButton>(UButton::StaticClass(), WidgetName);
	UTextBlock* LabelText = CreateNativeTextBlock(FName(*FString::Printf(TEXT("%s_Label"), *WidgetName.ToString())), Label, 13);
	LabelText->SetJustification(ETextJustify::Center);
	LabelText->SetColorAndOpacity(FSlateColor(OnokoGoldColor));
	Button->SetContent(LabelText);
	Button->SetColorAndOpacity(FLinearColor(1.0f, 1.0f, 1.0f, 0.96f));
	Button->SetBackgroundColor(OnokoBlueDimColor);
	return Button;
}

void UOnokoArcanaTableHudWidget::AddNativeButtonToRow(UHorizontalBox* Row, UButton* Button, const FMargin& InPadding)
{
	if (!Row || !Button)
	{
		return;
	}

	USizeBox* ButtonSizeBox = WidgetTree->ConstructWidget<USizeBox>(
		USizeBox::StaticClass(),
		FName(*FString::Printf(TEXT("%s_SizeBox"), *Button->GetName())));
	ButtonSizeBox->SetWidthOverride(70.0f);
	ButtonSizeBox->SetHeightOverride(34.0f);
	ButtonSizeBox->SetContent(Button);

	if (UHorizontalBoxSlot* ButtonSlot = Row->AddChildToHorizontalBox(ButtonSizeBox))
	{
		ButtonSlot->SetPadding(InPadding);
	}
}

void UOnokoArcanaTableHudWidget::AddNativeRow(UVerticalBox* Box, UWidget* Widget, const FMargin& InPadding)
{
	if (!Box || !Widget)
	{
		return;
	}

	if (UVerticalBoxSlot* RowSlot = Box->AddChildToVerticalBox(Widget))
	{
		RowSlot->SetPadding(InPadding);
	}
}
