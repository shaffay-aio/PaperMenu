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
- Remove background
- Rotate images to the correct orientation before uploading. (menu should be straight)
- Avoid blurry images.

#### Future Additions
- ⭕ Add Pydantic structure for output.
- ⭕ Quality testing on diverse menus.

#### Testing
- ⭕ Tilted menu tested.
- ⭕ Single pager straight menu tested.
- ⭕ Multi pager straight menu tested.
- Test on menus given in https://aioapp.atlassian.net/browse/AIS-549.

#### TODO
- Only categories and items (name, price, description) will be extracted in V1.
- Use gpt 40 mini to concat jsons.
- for gemini if there are multiple menu images, to certain number you can send them all at once and get one json 

lookup : If using a single image, place the text prompt after the image.