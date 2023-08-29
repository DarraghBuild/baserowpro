import { expect, Locator, Page } from "@playwright/test";
import { BaserowPage } from "./baserowPage";
import { Header } from "../components/gridHeader";

export class CalendarPage extends BaserowPage {
    private readonly searchButtonIcon: Locator;
    private readonly searchMatchCells: Locator;
    private readonly loadingOverlay: Locator;
    private readonly searchInput: Locator;
    readonly header: Header;

    constructor(page: Page) {
        super(page);
        this.header = new Header(page);
        this.searchButtonIcon = this.page.locator(".header__search-icon");
        this.searchMatchCells = this.page.locator(".calendar-card__labels");
        this.loadingOverlay = this.page.locator(".content .loading-overlay");
        this.searchInput = this.page.getByPlaceholder("Search in all rows");
    }

    async clearSearchInput() {
        await this.searchButtonIcon.click();
        await this.searchInput.click();
        await this.searchInput.fill("");

        await this.waitForLoadingOverlayToDisappear();
    }

    async openSearchContextAndSearchFor(searchTerm) {
        await this.searchButtonIcon.click();
        await this.searchInput.click();
        await this.searchInput.fill("");
        await this.page.keyboard.type(searchTerm.toString());
        await this.page.keyboard.press("Enter");
        await this.waitForLoadingOverlayToDisappear();
        await this.searchButtonIcon.click();
    }

    searchMatchingCells() {
        return this.searchMatchCells;
    }

    async waitForLoadingOverlayToDisappear() {
        await expect(this.loadingOverlay).toHaveCount(0);
    }
}
