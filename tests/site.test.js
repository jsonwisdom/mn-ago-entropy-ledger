import { describe, expect, it } from "vitest";
import { TestDriver } from "testdriverai/vitest/hooks";

describe("Global Truth OS", () => {
  it("loads the dashboard and displays claims and receipts", async (context) => {
    const testdriver = TestDriver(context);

    // Navigate to the production site
    await testdriver.provision.chrome({
      url: "https://jsonwisdom.github.io/mn-ago-entropy-ledger/site/",
    });

    // Verify the heading is visible
    const heading = await testdriver.find("GLOBAL TRUTH OS heading");
    expect(heading).toBeDefined();

    // Verify the stats section displays total counts
    const stats = await testdriver.find("stats summary showing TOTAL, RED, YELLOW, and GREEN");
    expect(stats).toBeDefined();

    // Verify that claims cards are rendered
    const claimCard = await testdriver.find("claim card");
    expect(claimCard).toBeDefined();

    // Click 'View Receipts' to inspect receipts for a claim
    const viewReceiptsButton = await testdriver.find("View Receipts button");
    await viewReceiptsButton.click();

    // Assert that the modal showing receipts is displayed
    const modalVisible = await testdriver.assert("a modal dialog showing receipts details is open");
    expect(modalVisible).toBeTruthy();

    // Dismiss the modal
    await testdriver.find("modal overlay or content").click();
  });
});
