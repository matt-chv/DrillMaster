/* DB upgrade v0.1 to v.2*/
PRAGMA encoding="UTF-8";
PRAGMA foreign_keys=off;

-- start a transaction
BEGIN TRANSACTION;

-- Here you can drop column
CREATE TABLE IF NOT EXISTS new_table (
    TIME TIMESTAMP,
    ANSWER TEXT,
    EXPECTED_ANSWER TEXT,
    TIME_TO_ANSWER INTEGER,
    TARGET_TIME_TO_ANSWER INTEGER,
    NUMBER_ATTEMPTS INTEGER,
    Q_ID INTEGER,
    U_ID INTEGER,
    FOREIGN KEY (Q_ID) REFERENCES questions(id),
    FOREIGN KEY (U_ID) REFERENCES users(id)
    );
-- copy data from the table to the new_table
INSERT INTO new_table(TIME, ANSWER, EXPECTED_ANSWER,TIME_TO_ANSWER,TARGET_TIME_TO_ANSWER )
SELECT TIME, ANSWER, EXPECTED_ANSWER,TIME_TO_ANSWER,TARGET_TIME_TO_ANSWER
FROM HISTORY;

-- drop the table
DROP TABLE HISTORY;

-- rename the new_table to the table
ALTER TABLE new_table RENAME TO HISTORY; 

-- commit the transaction
COMMIT;

-- enable foreign key constraint check
PRAGMA foreign_keys=on;
