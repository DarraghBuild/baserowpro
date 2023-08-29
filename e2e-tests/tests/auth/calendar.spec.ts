import { expect, test } from "@playwright/test";
import { LoginPage } from "../../pages/loginPage";
import { TablePage } from "../../pages/tablePage";
import { CalendarPage } from "../../pages/calendarPage";
import { DashboardPage } from "../../pages/dashboardPage";
import { createUser, deleteUser, getStaffUser } from "../../fixtures/user";
import { Sidebar } from "../../components/sidebar";
import { createRows, deleteRows } from "../../fixtures/rows";
import { createDatabase } from "../../fixtures/database";
import { createTable } from "../../fixtures/table";
import { getUsersFirstWorkspace } from "../../fixtures/workspace";
import { faker } from "@faker-js/faker";

import {
    createField,
    deleteAllNonPrimaryFieldsFromTable,
} from "../../fixtures/field";

let user:any = null;
const currentDate = new Date();

const firstDayCurrentMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    1
);
const lastDayCurrentMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    0
);

test.beforeEach(async () => {
    user = await createUser();
    const workspace = await getUsersFirstWorkspace(user);
    const database = await createDatabase(user, "calendarTestDB", workspace);
    const table = await createTable(user, "calendarTestTable", database);
    await deleteAllNonPrimaryFieldsFromTable(user, table);
    await createField(user, "Date", "date", {}, table);
    await deleteRows(user, table, [1, 2]);
    await createRows(user, table, [
        {
            id: 1,
            Name: "Summer Festival",
            Date: faker.date
                .between(firstDayCurrentMonth, lastDayCurrentMonth)
                .toISOString()
                .split("T")[0],
        },
        {
            id: 2,
            Name: "Tech Meetup",
            Date: faker.date
                .between(firstDayCurrentMonth, lastDayCurrentMonth)
                .toISOString()
                .split("T")[0],
        },
        {
            id: 3,
            Name: "Charity Run",
            Date: faker.date
                .between(firstDayCurrentMonth, lastDayCurrentMonth)
                .toISOString()
                .split("T")[0],
        },
        {
            id: 4,
            Name: "Tech Meetup",
            Date: faker.date
                .between(firstDayCurrentMonth, lastDayCurrentMonth)
                .toISOString()
                .split("T")[0],
        },
    ]);
});

test.afterEach(async () => {
    // We only want to bother cleaning up in a devs local env or when pointed at a real
    // server. If in CI then the first user will be the first admin and this will fail.
    // Secondly in CI we are going to delete the database anyway so no need to clean-up.
    if (!process.env.CI) {
        await deleteUser(user);
    }
});

async function setupCalendarView(page) {
    const tablePage = new TablePage(page);
    const genericModal = await tablePage.header.clickCalandarView();
    await genericModal.waitUntilLoaded();
    await genericModal.clickAddButton();
    await page.getByRole("button", { name: "Save" }).click();
}

test("User can search the calendar @calendar", async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginWithPassword(user.email, user.password);
    // Pass our user's token to the dashboard page's middleware, visit it.
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.authWithMiddleware(user);
    await dashboardPage.goto();
    await dashboardPage.checkOnPage();

    const sideBar = new Sidebar(page);
    await sideBar.selectDatabaseAndTableByName(
        "calendarTestDB",
        "calendarTestTable"
    );
    await setupCalendarView(page);

    const calendarPage = new CalendarPage(page);
    await page.pause();
    await expect(
        calendarPage.searchMatchingCells().getByText("Charity Run")
    ).toHaveCount(1);

    await calendarPage.openSearchContextAndSearchFor("Tech Meetup");
    await expect(
        calendarPage.searchMatchingCells().getByText("Tech Meetup")
    ).toHaveCount(2);
    await expect(
        calendarPage.searchMatchingCells().getByText("Charity Run")
    ).toHaveCount(0);
});
