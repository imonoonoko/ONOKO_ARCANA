#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Types/SlateEnums.h"
#include "OnokoArcanaTableHudWidget.generated.h"

class AOnokoArcanaTableController;
class UBorder;
class UButton;
class UComboBoxString;
class UEditableTextBox;
class UHorizontalBox;
class UMultiLineEditableTextBox;
class UTextBlock;
class UVerticalBox;
class UWidget;

UCLASS(BlueprintType, Blueprintable)
class ONOKO_ARCANA_API UOnokoArcanaTableHudWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<AOnokoArcanaTableController> TableController;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UEditableTextBox> QuestionTextBox;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> StartReadingButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> DrawButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> RevealCardButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UMultiLineEditableTextBox> UserInterpretationTextBox;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> RevealGuideButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> ResetButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> SaveReadingButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> RefreshHistoryButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UComboBoxString> SpreadSelectorComboBox;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> ActiveSpreadText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> SpreadSlotsText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> SelectedSpreadSlotText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> PastSlotButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> PresentSlotButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UButton> FutureSlotButton;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> CardTitleText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> OrientationText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> KeywordsText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> StudyFocusText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> ErrorText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> StateText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> HistoryCountText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> HistoryLatestSummaryText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> HistorySelectedTitleText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> HistorySelectedDetailText;

	UPROPERTY(meta = (BindWidgetOptional), BlueprintReadOnly, Category = "ONOKO Arcana|HUD")
	TObjectPtr<UTextBlock> HistoryEmptyStateText;

	virtual void NativeOnInitialized() override;

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SetTableController(AOnokoArcanaTableController* InTableController);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	bool FindTableControllerInWorld();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void RefreshFromController();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void StartReadingFromQuestion();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void DrawCard();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void RevealCard();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void RevealGuide();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void ResetTable();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SaveCurrentReading();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void RefreshReadingHistory();

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SelectHistoryReading(int32 Index);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SelectSpreadById(FName SpreadId);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SelectSpreadSlotById(FName PositionKey);

	UFUNCTION(BlueprintCallable, Category = "ONOKO Arcana|HUD")
	void SubmitUserInterpretationText(const FText& Text);

private:
	UFUNCTION()
	void HandleStartReadingClicked();

	UFUNCTION()
	void HandleDrawClicked();

	UFUNCTION()
	void HandleRevealCardClicked();

	UFUNCTION()
	void HandleRevealGuideClicked();

	UFUNCTION()
	void HandleResetClicked();

	UFUNCTION()
	void HandleSaveReadingClicked();

	UFUNCTION()
	void HandleRefreshHistoryClicked();

	UFUNCTION()
	void HandleUserInterpretationChanged(const FText& Text);

	UFUNCTION()
	void HandleSpreadSelectionChanged(FString SelectedItem, ESelectInfo::Type SelectionType);

	UFUNCTION()
	void HandlePastSlotClicked();

	UFUNCTION()
	void HandlePresentSlotClicked();

	UFUNCTION()
	void HandleFutureSlotClicked();

	static void SetTextIfBound(UTextBlock* TextBlock, const FString& Text);
	static void SetEnabledIfBound(UWidget* Widget, bool bEnabled);
	FString GetQuestionText() const;
	void RefreshSpreadSelectorOptions();
	static FString MakeSpreadOptionLabel(FName SpreadId, const FString& DisplayName, int32 CardCount);
	static FName ExtractSpreadIdFromOption(const FString& OptionLabel);
	void BuildNativeFallbackWidgetTreeIfNeeded();
	UBorder* CreateNativePanel(FName WidgetName, const FMargin& PanelPadding, const FLinearColor& BrushColor);
	UTextBlock* CreateNativeTextBlock(FName WidgetName, const FString& Text, int32 FontSize = 16);
	UTextBlock* CreateNativeSectionTitle(FName WidgetName, const FString& Text);
	UButton* CreateNativeButton(FName WidgetName, const FString& Label);
	void AddNativeButtonToRow(UHorizontalBox* Row, UButton* Button, const FMargin& InPadding = FMargin(0.0f, 0.0f, 8.0f, 0.0f));
	void AddNativeRow(UVerticalBox* Box, UWidget* Widget, const FMargin& InPadding = FMargin(0.0f, 0.0f, 0.0f, 8.0f));
};
