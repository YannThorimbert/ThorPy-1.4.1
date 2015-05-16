def run():
    import thorpy

    application = thorpy.Application((800, 600), "ThorPy Overview")

    #texts that summary the element's roles:
    text_element = "Element instance:\nMost simple graphical element."
    text_clickable = "Clickable instance:\nCan be hovered and pressed."
    text_draggable = "Draggable instance:\nYou can drag it."
    text_check = "Checker instance:\nHere it is of type 'checkbox'."
    text_radio = "Checker instance:\nHere it is of type 'radio'."
    text_browser = "Browser instance:\nFind a file or a folder on the computer."
    text_dropdownlist = "DropDownList:\nDisplay a list of choices."
    text_slider = "SliderX:\nA way for user to select a value.\n" +\
                    "Can be any type of number (int, float, bool, ..)"
    text_text = "Text:\nThis is just a raw element with a certain type of style."

    #actual declaration of the elements

    #this element has no effect : it contains nothing and it is a ghost
    ghost = thorpy.Ghost()
    ghost.finish()

    element = thorpy.Element("Element")
    element.finish()
    thorpy.makeup.add_basic_help(element, text_element)

    clickable = thorpy.Clickable("Clickable")
    clickable.finish()
    thorpy.makeup.add_basic_help(clickable, text_clickable)

    draggable = thorpy.Draggable("Draggable")
    draggable.finish()
    thorpy.makeup.add_basic_help(draggable, text_draggable)

    checker_check = thorpy.Checker("Checker")
    checker_check.finish()
    thorpy.makeup.add_basic_help(checker_check, text_check)

    checker_radio = thorpy.Checker("Radio", typ="radio")
    checker_radio.finish()
    thorpy.makeup.add_basic_help(checker_radio, text_radio)

    browser = thorpy.Browser("../../", text="Browser")
    browser.finish()

    browserlauncher = thorpy.BrowserLauncher(browser, name_txt="Browser",
                                           file_txt="Nothing selected",
                                           launcher_txt="...")
    browserlauncher.finish()
    browserlauncher.scale_to_title()
    thorpy.makeup.add_basic_help(browserlauncher, text_browser)

    dropdownlist = thorpy.DropDownListLauncher(name_txt="DropDownListLauncher",
                                             file_txt="Nothing selected",
                                             titles=[str(i) for i in range(1, 9)])
    dropdownlist.finish()
    dropdownlist.scale_to_title()
    thorpy.makeup.add_basic_help(dropdownlist, text_dropdownlist)

    slider = thorpy.SliderX(120, (5, 12), "Slider: ", typ=float, initial_value=8.4)
    slider.finish()
    thorpy.makeup.add_basic_help(slider, text_slider)

    inserter = thorpy.Inserter(name="Inserter: ", value="Write here.")
    inserter.finish()
    thorpy.makeup.add_basic_help(inserter,
                               "Inserter:\nA way for user to insert a value.")


    title_element = thorpy.make_text("Overview example", 22, (255,255,0))
    thorpy.makeup.add_basic_help(title_element, text_text)

    central_box = thorpy.Box("", [ghost, element, clickable, draggable, checker_check,
                                checker_radio, dropdownlist, browserlauncher,
                                slider, inserter])
    central_box.finish()
    central_box.center()
    central_box.add_lift()
    central_box.set_main_color((220,220,220,180))

    background = thorpy.Background(image=thorpy.style.EXAMPLE_IMG,
                                   elements=[title_element, central_box])
    background.finish()
    thorpy.store(background)

    menu = thorpy.Menu(background)
    menu.play()

    application.quit()



if __name__ == "__main__":
    run()
