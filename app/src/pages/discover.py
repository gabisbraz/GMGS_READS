from time import sleep
import flet as ft


def discover_livros(page: ft.Page):
    """
    Página para descobrir vários livros com informações básicas.
    Ao clicar em um livro, redireciona para a página de detalhes do livro.
    """
    page.title = "Auto-scrolling Book Grid"
    page.window.width = 480
    page.window.height = 800
    page.window.resizable = False
    page.theme = ft.Theme(color_scheme_seed="green")
    page.theme_mode = "light"

    # Create a GridView for books
    grid_view = ft.GridView(spacing=10, runs_count=3, max_extent=150, expand=True)

    # Static list of livros data
    livros = [
        {
            "title": f"Book {i+1}",
            "authors": f"Author {chr(65+i)}",
            "bookID": i + 1,
            "image_path": "image.jpg",
        }
        for i in range(15)  # Generate 15 books for demonstration
    ]

    # Add initial book items to the GridView
    for livro in livros:
        grid_view.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(livro["title"], size=18, weight="bold"),
                        ft.Image(src=livro["image_path"], width=100),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border_radius=10,
            )
        )

    page.add(grid_view)

    # Dynamically add more books to the GridView every second
    count = len(livros) + 1  # Start from the next book ID
    for i in range(5):  # Add 5 more books as an example
        sleep(1)  # Wait for 1 second
        new_book = {
            "title": f"New Book {count}",
            "authors": f"New Author {chr(65 + (count-1))}",
            "bookID": count,
            "image_path": "image.jpg",
        }
        grid_view.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(new_book["title"], size=18, weight="bold"),
                        ft.Image(src=new_book["image_path"], width=100),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border_radius=10,
            )
        )
        count += 1
        page.update()  # Update the page to show the new content


ft.app(discover_livros)
