# Fungus-Field Blog Archive

The blogs are rendered in Typora style

## Usage

1. Go to your `.md` file in Typora

2. Click on `File`->`Export`->`HTML (without styles)` and save the exported `.html` file in whatever folder you like

3. Open the exported `.html` and copy the code of the notes

    ```html
    <!-- ... -->
    <body>

        <!-- Copy the HTML code here -->

    </body>
    <!-- ... -->
    ```

4. Create a new post folder using the template in `/posts/template`

5. Paste the copied code in the `index.html` in the `/template`
    
    ```html
    <!-- ... -->
    <div class="post-content typora-content">

        <!-- Paste the copied HTML code here -->
        
    </div>
    <!-- ... -->
    ```

6. Add a new entry to `posts.json` and configure as desired

    ```json
    {
        "title": "BLOG_NAME",
        "date": "YYYY-MM-DD",
        "url": "posts/NEW_POST_FOLDER",
        "summary": "WRITE_WHATEVER_YOU_LIKE_HERE",
        "tags": ["TAG_1", "TAG_2", "TAG_N"]
    }
    ```

7. Run the generator, then you are all set!

    ```bash
    python scripts/generate-list-pages.py
    ```