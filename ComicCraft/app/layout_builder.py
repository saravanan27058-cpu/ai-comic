def build_comic_layout(stories, image_paths):
    layout = []

    for story, image_path in zip(stories, image_paths):
        item = story.model_dump()
        item["image_path"] = image_path
        layout.append(item)

    return layout
