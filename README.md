#### Models
- Gemini
- Qwen
- Gpt

#### Target Menus
- Pamphlet Menus – Single-sheet, foldable, or takeaway menus often used for promotions and delivery.
- Booklet Menus  – Multi-page, bound menus used in sit-down restaurants.

#### Components
- VLM  : extracts menu in structured format
- SM   : fills modifiers and options
- LLM  : refines m/o 

#### Flow
- Upload single pager menu.
- Read it via OCR. (prompt (quality, template), model, json)
- Output should be json. (Category, Item, Price, Description)
- It will not have Modifier/Option
- Get scraped menu.
- Embedding based similarity matching and modifier/option attahcement.
- Super Menu enhancement.
- Convert to AIO format.

- For multi pager, read all one by one.
- Use gpt 40 mini to concat jsons.