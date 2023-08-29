import { Locator, Page } from "@playwright/test";
import { GenericModal } from "./genericModal";

export class Header {
    page: Page;
    private readonly viewsButton: Locator;
    private readonly createCalendarButton: Locator;
    private readonly addCalendarButton;
    private readonly saveCalendarButton;

    constructor(page: Page) {
        this.page = page;
        this.viewsButton = this.page
            .locator('.header__filter-item--grids')
        this.createCalendarButton = page.getByText("Calendar").first();
    }

    async clickViewsButton() {
        await this.viewsButton.click();
    }
    clickCreateCalendarButton() {
        return this.createCalendarButton.click();
    }

    async clickCalandarView(): Promise<GenericModal> {
        await this.clickViewsButton();
        await this.clickCreateCalendarButton();
        return new GenericModal(this.page);
    }
}
