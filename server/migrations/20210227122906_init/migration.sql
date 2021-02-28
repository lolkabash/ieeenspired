-- CreateTable
CREATE TABLE "Chemical" (
    "id" TEXT NOT NULL,
    "substance" TEXT NOT NULL,
    "identifier" TEXT NOT NULL,
    "scope" TEXT NOT NULL,
    "threshold" TEXT NOT NULL,
    "exemptions" TEXT NOT NULL,
    "reference" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "Chemical.id_unique" ON "Chemical"("id");
