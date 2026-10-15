# Fungus-Field Blog Archive

The blogs use static HTML with scoped support for Typora exports.

The visual theme takes typography and color inspiration from [SGS](https://sgs-rl.github.io/): a black navigation bar, white reading surface, vermilion accents, and an asymmetric topic index in yellow, pink, cobalt, and mint. Topic counts come from `posts.json`; the featured topic labels live in `HOME_TOPICS` in the generator. `tokens.css` holds the light/dark palette, typography, and spacing. The final section of `assets/css/style.css` adapts these tokens to the existing pages. Inter and Inter Tight are self-hosted in `assets/fonts/` with their OFL licenses; Chinese text uses the system font fallback.

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
