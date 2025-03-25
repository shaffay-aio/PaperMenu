#### Usage Commands
```
pip install -r requirements.txt
python app.py
```

#### Models
1. Gemini 2.0 Flash
2. Qwen VL Max (VPN required)
3. Gpt 4o

#### Target Menus
- Pamphlet Menus – Single-sheet, foldable, or takeaway menus often used for promotions and delivery.
- Booklet Menus  – Multi-page, bound menus used in sit-down restaurants.

#### Components
- VLM  : extracts menu in structured format
- SM   : fills modifiers and options
- LLM  : refines m/o 

#### Performance Enhancement
- Explore image restructuring
- Any additional information we can extract from menu

#### Performance Eval
- Are all categories, items being fetched?
- Are their any spelling errors?
- Is there any irrelevant information being fetched?

#### Menu Instructions
- Rotate images to the correct orientation before uploading.
- Avoid blurry images.

#### Future Additions
- ⭕ Convert to AIO format.
- ⭕ Add Pydantic structure for output.
- ⭕ Add multi jpgs, pdf to api input.
- ⭕ Add error handling.
- ⭕ Quality testing on diverse menus.
- ⭕ Super Menu enhancement.

#### TODO
- For multi pager, read all one by one.
- Use gpt 40 mini to concat jsons.
- for gemini if there are multiple menu images, to certain number you can send them all at once and get one json 

- add appropiate logging
- resolve super menu and other api file recieving issue via api
- improve prompt by fixing output format, telling what information to extract

lookup : If using a single image, place the text prompt after the image.