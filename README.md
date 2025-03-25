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
x-1. enable logging
x2. add gemini
3. define pydantic output structure
4. add aio format
5. super menu apis


x- Upload single pager menu.
x- Read it via OCR. (prompt (quality, template), model (qwen, gemini, ), json (llm, extractor))
x- Output should be json. (Category, Item, Price, Description)
- Pydantic structure for json validator
x- It will not have Modifier/Option
x- Get scraped menu.
x- Embedding based similarity matching and modifier/option attachement.
- Convert to AIO format.
- Super Menu enhancement.

- For multi pager, read all one by one.
- Use gpt 40 mini to concat jsons.
- for gemini if there are multiple menu images, to certain number you can send them all at once and get one json 

- add appropiate logging
- resolve super menu and other api file recieving issue via api
- improve prompt by fixing output format, telling what information to extract

lookup : If using a single image, place the text prompt after the image.

#### Performance Enhancement
- Explore image restructuring
- Any additional information we can extract from menu

#### Menu Instructions
- Rotate images to the correct orientation before uploading.
- Avoid blurry images.

#### Future Additions
- ⭕ Add multi jpgs, pdf to api input.
- ⭕ Add error handling.
- ⭕ Fill default values of newly added items.

#### Usage Commands
```
pip install -r requirements.txt
python app.py
```