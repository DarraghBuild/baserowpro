import { Locator, Page } from "@playwright/test";

export class GenericModal {
    private readonly page: Page;
    private readonly databaseBodyLayout: Locator;
    private readonly addButton: Locator;

    constructor(page: Page) {
        this.page = page;
        this.databaseBodyLayout = this.page.locator(".modal__box");
        this.addButton = this.page.getByText(/ Add /);
    }

    async waitUntilLoaded() {
        await this.databaseBodyLayout.waitFor();
    }

    async clickAddButton() {
        await this.addButton.click();
    }
}
