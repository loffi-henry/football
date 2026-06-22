# 角色模型資料夾（GLB）

把產好的模型放這裡，**檔名必須完全一致**，重整網頁就會自動換成新模型：

```
models/Shooter.glb       ← 射手（紅衣 #10）
models/Goalkeeper.glb    ← 守門員（黃/綠衣 #1）
```

沒有檔案時，遊戲會自動沿用內建的幾何體角色（不會壞）。

---

## 我（Claude）已經做好的部分

- `GLTFLoader` 載入 + `AnimationMixer` 播放內嵌動畫
- 遊戲狀態已接好動畫：
  - 射手：`idle` → 射門時 `kick` → 進球 `celebrate`
  - 守門員：`idle` → 撲救 `Dive Left` / `Dive Right` → 沒撲到 `Jump Save`
- 自動依目標身高縮放、對齊地面、朝向校正
- 找不到檔案時自動 fallback 到幾何體角色

> 動畫片段名稱寫在 `index.html` 的 `CHAR_MODELS` 設定區。
> 你的 GLB 匯出後，把實際的片段名稱（在瀏覽器主控台會印出 `[model] 已載入 ... 動畫：[...]`）填進 `clips` 即可對上。

---

## 你（人）要做的部分：產生 GLB

我無法自行生成雕刻級 3D 模型，請用下列任一條流程，把 `q版3d足球角色設計prompt.md` 的設計圖餵進去：

### 流程 A：image-to-3D（最快）
1. 到 **Meshy.ai** 或 **Tripo3D** 或 **Rodin (hyper3d.ai)**
2. 用「Image to 3D」上傳設計圖（射手、守門員各一張）
3. 開啟 **Auto-rig / Animation**（若該工具支援），輸出 **GLB**

### 流程 B：生模型 + Mixamo 綁骨動畫（動畫最穩）
1. 用流程 A 的工具只生「模型」(T-pose 最佳)，輸出 FBX/GLB
2. 上傳到 **Mixamo (mixamo.com，Adobe 免費)** → 自動 humanoid 綁骨
3. 套用動畫並下載：
   - 射手：`Idle`、`Kick`(或 Soccer Pass/Shot)、`Celebrate`
   - 守門員：`Idle`、`Goalkeeper Dive Left`、`Dive Right`、`Jump`
4. 用 Blender 把多個動畫合進同一個檔，匯出 **GLB（glTF 2.0，含動畫、嵌入貼圖）**

### 規格（給生成工具參考）
- 風格：Chibi 2.3 頭身、Mobile game、乾淨 PBR
- 身高 1.2m、+Y up、+Z forward、pivot 底部中心
- 3,500–5,000 tris、2048² 貼圖
- 射手：紅衣白褲紅襪黑鞋 #10；守門員：黃/綠衣黑褲 #1、放大白手套

拿到 `Shooter.glb` / `Goalkeeper.glb` 丟進這個資料夾就完成了。對不上的話把主控台印出的動畫名稱貼給我，我幫你改 `clips` 對應。
