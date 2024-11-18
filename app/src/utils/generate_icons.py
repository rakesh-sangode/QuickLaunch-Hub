from PIL import Image, ImageDraw

def create_plus_icon(size=32, color=(0, 157, 255)):
    # Create a new image with a transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    line_width = max(3, size // 12)  # Thicker lines
    margin = size // 4
    
    # Draw plus symbol
    # Horizontal line
    draw.rectangle(
        [margin, (size-line_width)//2, size-margin, (size+line_width)//2],
        fill=color
    )
    
    # Vertical line
    draw.rectangle(
        [(size-line_width)//2, margin, (size+line_width)//2, size-margin],
        fill=color
    )
    
    return img

def create_minus_icon(size=32, color=(255, 69, 58)):
    # Create a new image with a transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    line_width = max(3, size // 12)  # Thicker lines
    margin = size // 4
    
    # Draw minus symbol
    draw.rectangle(
        [margin, (size-line_width)//2, size-margin, (size+line_width)//2],
        fill=color
    )
    
    return img

def create_select_all_icon(size=32, color=(52, 53, 65)):
    # Create a new image with a transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    line_width = max(2, size // 12)
    margin = size // 6
    box_size = size - (2 * margin)
    
    # Draw outer square
    draw.rectangle(
        [margin, margin, margin + box_size, margin + box_size],
        outline=color,
        width=line_width
    )
    
    # Draw checkmark inside
    check_margin = margin + (box_size // 4)
    check_width = max(2, line_width)
    
    # Draw checkmark
    points = [
        (check_margin, margin + box_size//2),  # Left point
        (margin + box_size//2, margin + box_size - check_margin + line_width),  # Bottom point
        (margin + box_size - check_margin + line_width, check_margin)  # Top right point
    ]
    draw.line(points, fill=color, width=check_width)
    
    return img

def create_unselect_all_icon(size=32, color=(52, 53, 65)):
    # Create a new image with a transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    line_width = max(2, size // 12)
    margin = size // 6
    box_size = size - (2 * margin)
    
    # Draw outer square
    draw.rectangle(
        [margin, margin, margin + box_size, margin + box_size],
        outline=color,
        width=line_width
    )
    
    return img

def generate_icons():
    # Create icons directory if it doesn't exist
    import os
    icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate and save icons
    plus_icon = create_plus_icon()
    minus_icon = create_minus_icon()
    select_all_icon = create_select_all_icon()
    unselect_all_icon = create_unselect_all_icon()
    
    plus_icon.save(os.path.join(icons_dir, 'add.png'))
    minus_icon.save(os.path.join(icons_dir, 'remove.png'))
    select_all_icon.save(os.path.join(icons_dir, 'select_all.png'))
    unselect_all_icon.save(os.path.join(icons_dir, 'unselect_all.png'))

if __name__ == '__main__':
    generate_icons()
