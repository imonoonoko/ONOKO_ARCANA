(() => {
const SOURCE_ASSET_ROOT = "../assets/generated/card-production-v5-full/alpha/";
const WEB_CARD_ROOT = "../assets/generated/card-production-v5-full/web-labeled/alpha/";

const CARD_BACK = `${WEB_CARD_ROOT}card-back-onoko-v5-alpha.png`;

const ROMAN_NUMERALS = {
  "00": "0",
  "01": "I",
  "02": "II",
  "03": "III",
  "04": "IV",
  "05": "V",
  "06": "VI",
  "07": "VII",
  "08": "VIII",
  "09": "IX",
  "10": "X",
  "11": "XI",
  "12": "XII",
  "13": "XIII",
  "14": "XIV",
  "15": "XV",
  "16": "XVI",
  "17": "XVII",
  "18": "XVIII",
  "19": "XIX",
  "20": "XX",
  "21": "XXI"
};

const CARD_ROWS = [
  ["00", "fool", "愚者", "The Fool", ["始まり", "自由", "可能性", "冒険"], ["無計画", "軽率", "迷走", "準備不足"], "まだ形になっていない可能性を、恐れすぎず観測し始める。"],
  ["01", "magician", "魔術師", "The Magician", ["意志", "起動", "技術", "具現化"], ["空回り", "未熟", "操作", "集中不足"], "手元にある道具を把握し、意志を行動へ変換する。"],
  ["02", "high-priestess", "女教皇", "The High Priestess", ["直感", "記録", "沈黙", "深層"], ["閉鎖", "不信", "見落とし", "秘密過多"], "すぐ結論を出さず、静かな違和感や内側の記録を読む。"],
  ["03", "empress", "女帝", "The Empress", ["創造", "豊かさ", "育成", "美"], ["過保護", "停滞", "浪費", "消耗"], "育てる対象、環境、身体感覚が十分に満たされているかを見る。"],
  ["04", "emperor", "皇帝", "The Emperor", ["構造", "責任", "統率", "境界"], ["支配", "硬直", "独断", "無責任"], "守るべき枠組みと、硬くなりすぎている枠組みを分ける。"],
  ["05", "hierophant", "教皇", "The Hierophant", ["学び", "伝統", "助言", "約束"], ["形式主義", "反発", "盲信", "孤立"], "独学では見えない基準、師、共同体の知恵を確認する。"],
  ["06", "lovers", "恋人", "The Lovers", ["選択", "調和", "価値観", "結びつき"], ["不一致", "依存", "迷い", "不誠実"], "惹かれるものと、本当に選びたい価値が一致しているかを見る。"],
  ["07", "chariot", "戦車", "The Chariot", ["前進", "制御", "勝利", "集中"], ["暴走", "分散", "停滞", "強引"], "勢いを止めず、進む方向と制御方法を同時に確認する。"],
  ["08", "strength", "力", "Strength", ["勇気", "忍耐", "優しさ", "自制"], ["萎縮", "怒り", "不安", "自信不足"], "力で押し切る場面か、落ち着いて手なずける場面かを見極める。"],
  ["09", "hermit", "隠者", "The Hermit", ["内省", "探求", "孤独", "導き"], ["孤立", "閉じこもり", "迷子", "拒絶"], "周囲の声を一度静めて、自分の中の灯りを探す。"],
  ["10", "wheel-of-fortune", "運命の輪", "Wheel of Fortune", ["転機", "循環", "流れ", "好機"], ["停滞", "抵抗", "不運", "周期の読み違い"], "今は押す時か、流れが変わるのを読む時かを観測する。"],
  ["11", "justice", "正義", "Justice", ["公平", "判断", "真実", "結果"], ["偏り", "不正", "責任回避", "誤判定"], "感情と事実を分け、選択の結果を正面から見る。"],
  ["12", "hanged-man", "吊された男", "The Hanged Man", ["停止", "視点転換", "受容", "保留"], ["無駄な我慢", "停滞", "被害者意識", "先延ばし"], "動けない時間を、見方を変えるための観測時間にする。"],
  ["13", "death", "死神", "Death", ["終了", "変容", "手放し", "再生"], ["執着", "変化拒否", "未完了", "停滞"], "何を終わらせることで、次の形が始まるのかを見る。"],
  ["14", "temperance", "節制", "Temperance", ["調整", "統合", "癒し", "中庸"], ["偏り", "不調和", "過剰", "混乱"], "混ぜるべきもの、分けるべきもの、整える速度を観察する。"],
  ["15", "devil", "悪魔", "The Devil", ["執着", "誘惑", "影", "依存"], ["解放", "自覚", "鎖を外す", "回復"], "外から縛られているのか、自分で握りしめているのかを見る。"],
  ["16", "tower", "塔", "The Tower", ["崩壊", "衝撃", "露見", "リセット"], ["崩壊回避", "遅延", "抵抗", "小さな警告"], "壊れたものではなく、壊れる前提が何だったかを読む。"],
  ["17", "star", "星", "The Star", ["希望", "回復", "信頼", "導き"], ["失望", "疑い", "疲労", "見失い"], "すぐ届く結果ではなく、長く頼れる光を見つける。"],
  ["18", "moon", "月", "The Moon", ["夢", "不安", "幻想", "無意識"], ["霧が晴れる", "誤解", "混乱の減少", "現実確認"], "不安そのものより、不安が映し出している影を読む。"],
  ["19", "sun", "太陽", "The Sun", ["成功", "喜び", "明快", "活力"], ["過信", "陰り", "遅れ", "素直さ不足"], "隠さず見えるもの、まっすぐ喜べるものを確認する。"],
  ["20", "judgement", "審判", "Judgement", ["覚醒", "呼びかけ", "再評価", "復活"], ["先送り", "自己否定", "聞き逃し", "未決"], "過去の結果を責めるのではなく、次に応答すべき声を探す。"],
  ["21", "world", "世界", "The World", ["完成", "統合", "到達", "循環完了"], ["未完成", "閉じきれない", "停滞", "次への不安"], "ここまでで完了したことと、次の循環へ持ち越すものを分ける。"]
];

const CARD_STUDY_DETAILS = {
  fool: {
    symbols: ["旅立ち", "白い花", "崖", "小さな荷物"],
    commonMisreads: ["無責任だけで読む", "準備不足をすべて否定する"],
    reflectionQuestions: ["今、まだ試していない可能性は何か。", "自由と無計画を分ける基準は何か。"]
  },
  magician: {
    symbols: ["机上の道具", "片手を天へ", "無限大", "赤と白"],
    commonMisreads: ["才能だけで結果が出ると読む", "操作性と創造性を混同する"],
    reflectionQuestions: ["手元にある道具は何か。", "意志を最初の行動に変えるなら何をするか。"]
  },
  "high-priestess": {
    symbols: ["柱", "幕", "月", "巻物"],
    commonMisreads: ["沈黙を停滞だけで読む", "直感を確認不要の結論にする"],
    reflectionQuestions: ["まだ言語化できない違和感は何か。", "今は開く情報と伏せる情報をどう分けるか。"]
  },
  empress: {
    symbols: ["実り", "庭", "母性", "金星"],
    commonMisreads: ["豊かさを消費だけで読む", "育成と過保護を区別しない"],
    reflectionQuestions: ["何を育てる時期か。", "満たされているものと枯れているものは何か。"]
  },
  emperor: {
    symbols: ["玉座", "王冠", "石", "境界線"],
    commonMisreads: ["支配と責任を混同する", "硬さをすべて悪く読む"],
    reflectionQuestions: ["守るべき枠組みは何か。", "誰が責任を持つべき場面か。"]
  },
  hierophant: {
    symbols: ["師", "鍵", "祝福", "門弟"],
    commonMisreads: ["伝統を盲信だけで読む", "学びの共同体を依存と決めつける"],
    reflectionQuestions: ["参照すべき基準や師は何か。", "型を守ることと破ることの境目はどこか。"]
  },
  lovers: {
    symbols: ["二者", "天使", "選択", "裸の正直さ"],
    commonMisreads: ["恋愛成就だけで読む", "選択の責任を軽く見る"],
    reflectionQuestions: ["本当に選んでいる価値は何か。", "惹かれるものと約束できるものは一致しているか。"]
  },
  chariot: {
    symbols: ["戦車", "二つの力", "鎧", "都市の外"],
    commonMisreads: ["前進を強引さと同一視する", "制御が不要な勢いと読む"],
    reflectionQuestions: ["進む方向は一つに絞れているか。", "両立させるべき二つの力は何か。"]
  },
  strength: {
    symbols: ["獅子", "手なずける手", "無限大", "静かな勇気"],
    commonMisreads: ["力を攻撃性だけで読む", "優しさを弱さとして読む"],
    reflectionQuestions: ["押すよりなだめるべき対象は何か。", "勇気と忍耐のどちらが必要か。"]
  },
  hermit: {
    symbols: ["灯り", "杖", "山", "外套"],
    commonMisreads: ["孤独を孤立だけで読む", "内省を行動回避にする"],
    reflectionQuestions: ["自分だけが確認できる灯りは何か。", "一度距離を置くべき声は何か。"]
  },
  "wheel-of-fortune": {
    symbols: ["輪", "四方の存在", "回転", "周期"],
    commonMisreads: ["幸運か不運だけで読む", "流れを待つだけの受け身にする"],
    reflectionQuestions: ["今はどの周期の中にいるか。", "流れが来た時に動ける準備は何か。"]
  },
  justice: {
    symbols: ["天秤", "剣", "法衣", "正面性"],
    commonMisreads: ["罰だけで読む", "公平さと冷淡さを混同する"],
    reflectionQuestions: ["事実と感情を分けるなら何が残るか。", "選択の結果を誰が受け取るか。"]
  },
  "hanged-man": {
    symbols: ["逆さの姿勢", "吊るされた足", "光輪", "停止"],
    commonMisreads: ["我慢すればよいと読む", "停止を失敗だけで読む"],
    reflectionQuestions: ["視点を逆にすると何が見えるか。", "保留する価値のある判断は何か。"]
  },
  death: {
    symbols: ["旗", "白い馬", "沈む太陽", "終わりの門"],
    commonMisreads: ["物理的な死と短絡する", "終了の痛みだけで読み再生を見ない"],
    reflectionQuestions: ["終わらせると空く場所はどこか。", "手放すことで始まるものは何か。"]
  },
  temperance: {
    symbols: ["二つの杯", "水の流れ", "片足ずつ", "中庸"],
    commonMisreads: ["妥協だけで読む", "調整に必要な時間を軽視する"],
    reflectionQuestions: ["混ぜるべきものと分けるべきものは何か。", "無理なく続く速度はどれくらいか。"]
  },
  devil: {
    symbols: ["鎖", "影", "欲望", "束縛"],
    commonMisreads: ["外部の悪だけに責任を置く", "欲望そのものを全否定する"],
    reflectionQuestions: ["外せるのに外していない鎖は何か。", "快楽と依存の境目はどこか。"]
  },
  tower: {
    symbols: ["落雷", "崩れる塔", "落下", "露見"],
    commonMisreads: ["破壊を罰だけで読む", "小さな警告を無視する"],
    reflectionQuestions: ["崩れる前提は何だったか。", "早めに崩した方がよい構造は何か。"]
  },
  star: {
    symbols: ["星", "水を注ぐ人", "裸の信頼", "遠い光"],
    commonMisreads: ["希望を即効性のある結果にする", "癒しを現実逃避にする"],
    reflectionQuestions: ["長く頼れる光は何か。", "回復のために水を注ぐ場所はどこか。"]
  },
  moon: {
    symbols: ["月", "道", "犬と狼", "水から出るもの"],
    commonMisreads: ["不安をすべて直感と見る", "曖昧さをすぐ悪い兆しにする"],
    reflectionQuestions: ["不安が映している影は何か。", "現実確認できる情報は何か。"]
  },
  sun: {
    symbols: ["太陽", "子ども", "白馬", "ひまわり"],
    commonMisreads: ["成功を過信に変える", "明るさで影を無視する"],
    reflectionQuestions: ["素直に喜べる成果は何か。", "隠さず見せることで進むものは何か。"]
  },
  judgement: {
    symbols: ["呼びかけ", "復活", "ラッパ", "再評価"],
    commonMisreads: ["裁きだけで読む", "過去の責め直しにする"],
    reflectionQuestions: ["今、応答すべき呼びかけは何か。", "過去の結果から次に使えるものは何か。"]
  },
  world: {
    symbols: ["輪", "踊る姿", "四隅の存在", "完成した循環"],
    commonMisreads: ["終わりを固定化する", "未完成な部分を失敗扱いする"],
    reflectionQuestions: ["完了した循環は何か。", "次の旅へ持ち越す経験は何か。"]
  }
};

const cards = CARD_ROWS.map(([number, slug, japaneseName, englishName, uprightKeywords, reversedKeywords, studyFocus]) => ({
  id: `major-${number}-${slug}`,
  number,
  displayNumber: ROMAN_NUMERALS[number] || number,
  slug,
  japaneseName,
  englishName,
  uprightKeywords,
  reversedKeywords,
  studyFocus,
  studyDetails: CARD_STUDY_DETAILS[slug] || {
    symbols: [],
    commonMisreads: [],
    reflectionQuestions: []
  },
  sourceImage: `${SOURCE_ASSET_ROOT}major-${number}-${slug}-onoko-v5-alpha.png`,
  image: `${WEB_CARD_ROOT}major-${number}-${slug}-onoko-v5-alpha.png`
}));

const spreads = [
  {
    id: "one_card",
    label: "一枚引き",
    description: "ひとつの問いに対して、今見るべき視点を一枚で読む。",
    layoutType: "single",
    slots: [
      { key: "present", label: "一枚引き", revealOrder: 1, prompt: "問い全体の焦点として読む。", x: 50, y: 50, rot: 0 }
    ]
  },
  {
    id: "three_card_past_present_future",
    label: "過去・現在・未来",
    description: "状況の流れを三段階で読み、変化の筋道を確認する。",
    layoutType: "linear",
    slots: [
      { key: "past", label: "過去", revealOrder: 1, prompt: "現在に影響している背景や前提を見る。", x: 18, y: 52, rot: -5 },
      { key: "present", label: "現在", revealOrder: 2, prompt: "今の中心課題や意識すべき状態を見る。", x: 50, y: 48, rot: 0 },
      { key: "future", label: "未来", revealOrder: 3, prompt: "この流れの先に出やすい可能性を見る。", x: 82, y: 52, rot: 5 }
    ]
  },
  {
    id: "five_card_cross",
    label: "五枚クロス",
    description: "中心課題、支え、障害、上位視点、根底を十字に読む。",
    layoutType: "cross",
    slots: [
      { key: "center", label: "中心", revealOrder: 1, prompt: "問いの中心にある主題を見る。", x: 50, y: 52, rot: 0 },
      { key: "support", label: "支え", revealOrder: 2, prompt: "助けになる資質や味方を見る。", x: 24, y: 52, rot: -6 },
      { key: "challenge", label: "障害", revealOrder: 3, prompt: "妨げや誤解されやすい点を見る。", x: 76, y: 52, rot: 6 },
      { key: "higher_view", label: "上位視点", revealOrder: 4, prompt: "一段高い視点から意味を読む。", x: 50, y: 20, rot: 0 },
      { key: "root", label: "根底", revealOrder: 5, prompt: "根底にある動機や未整理の感情を見る。", x: 50, y: 84, rot: 0 }
    ]
  },
  {
    id: "seven_card_horseshoe",
    label: "七枚ホースシュー",
    description: "過去から助言までを弧状に並べ、流れと選択肢を読む。",
    layoutType: "horseshoe",
    slots: [
      { key: "past", label: "過去", revealOrder: 1, prompt: "この問いに至った過去の流れを見る。", x: 11, y: 84, rot: -13 },
      { key: "present", label: "現在", revealOrder: 2, prompt: "現在の状況と課題を見る。", x: 24, y: 62, rot: -8 },
      { key: "hidden_influence", label: "隠れた影響", revealOrder: 3, prompt: "見落としている影響や前提を見る。", x: 37, y: 38, rot: -4 },
      { key: "obstacle", label: "障害", revealOrder: 4, prompt: "進行を妨げる要因を見る。", x: 50, y: 15, rot: 0 },
      { key: "outside", label: "周囲", revealOrder: 5, prompt: "周囲の反応や環境を見る。", x: 63, y: 38, rot: 4 },
      { key: "action", label: "行動", revealOrder: 6, prompt: "次に取るべき行動の方向を見る。", x: 76, y: 62, rot: 8 },
      { key: "outcome", label: "結果", revealOrder: 7, prompt: "このまま進んだ時の着地点を見る。", x: 89, y: 84, rot: 13 }
    ]
  },
  {
    id: "celtic_cross",
    label: "ケルト十字",
    description: "問題の核心、内外の影響、希望、結果までを広く読む十枚展開。",
    layoutType: "celtic_cross",
    slots: [
      { key: "present", label: "現状", revealOrder: 1, prompt: "問いの現在地を見る。", x: 34, y: 55, rot: 0 },
      { key: "crossing", label: "交差", revealOrder: 2, prompt: "現状に交差する課題や力を見る。", x: 50, y: 55, rot: 0 },
      { key: "root", label: "根底", revealOrder: 3, prompt: "根にある原因や無意識を見る。", x: 34, y: 84, rot: 0 },
      { key: "past", label: "過去", revealOrder: 4, prompt: "過ぎた影響を見る。", x: 18, y: 55, rot: -3 },
      { key: "crown", label: "意識", revealOrder: 5, prompt: "表層の意識や目標を見る。", x: 34, y: 26, rot: 0 },
      { key: "near_future", label: "近未来", revealOrder: 6, prompt: "近い未来の展開を見る。", x: 66, y: 55, rot: 3 },
      { key: "self", label: "自分", revealOrder: 7, prompt: "自分自身の姿勢を見る。", x: 84, y: 86, rot: 0 },
      { key: "environment", label: "環境", revealOrder: 8, prompt: "周囲や外部環境を見る。", x: 84, y: 62, rot: 0 },
      { key: "hopes_fears", label: "希望と不安", revealOrder: 9, prompt: "期待と恐れの両面を見る。", x: 84, y: 38, rot: 0 },
      { key: "outcome", label: "結果", revealOrder: 10, prompt: "総合的な着地点を見る。", x: 84, y: 14, rot: 0 }
    ]
  },
  {
    id: "relationship_line",
    label: "関係性ライン",
    description: "二者の状態、接点、課題、可能性を横並びに読む。",
    layoutType: "relationship",
    slots: [
      { key: "self", label: "自分", revealOrder: 1, prompt: "自分側の状態を見る。", x: 24, y: 38, rot: -4 },
      { key: "other", label: "相手", revealOrder: 2, prompt: "相手側の状態を見る。", x: 50, y: 38, rot: 0 },
      { key: "bridge", label: "接点", revealOrder: 3, prompt: "二者をつなぐものを見る。", x: 76, y: 38, rot: 4 },
      { key: "challenge", label: "課題", revealOrder: 4, prompt: "関係性の課題を見る。", x: 24, y: 70, rot: -4 },
      { key: "advice", label: "助言", revealOrder: 5, prompt: "関係性を扱う助言を見る。", x: 50, y: 70, rot: 0 },
      { key: "potential", label: "可能性", revealOrder: 6, prompt: "関係性の可能性を見る。", x: 76, y: 70, rot: 4 }
    ]
  }
];

window.OnokoArcanaData = {
  CARD_BACK,
  cards,
  spreads
};
})();
