---
layout: post
title:  "Alder v2.1.0"
date:   2024-10-18 10:10:00 -0500
categories: jekyll update
---
This is the official AlderBot v2.1.0 release. This release introduces simple reminders. Reminders are simply a way for a user to reminded about something specific. When a user sets a reminder, Alder will send them a direct message at the time of the reminder. With the current implementation, users can create single-time reminders, daily reminders, weekly reminders, and monthly reminders.

[Download Alder on GitHub](https://github.com/narlock/Alder)

### Alder API
- Requests related to timezone and reminders have been added.

## Features
- `/timezone` allows the user to view or set their timezone. Using `/timezone` without any parameters will return the user's current timezone. By default, this is UTC. By passing a timezone parameter. For example, `America/Chicago` - the full command being `/timezone America/Chicago`, the user's timezone will be set to Chicago time.
- `/reminders` command has been added for users to view and create reminders.
    - Passing no parameters will display all of the user's reminders.
    - For creating reminders, `title`, `remind_date`, and `remind_time` are **required**.
        - `/reminders title:My Reminder remind_date:2024-10-05 remind_time:17:00` is an example on how to set a single-occurrence reminder called "My Reminder". The `remind_time` parameter will be with respect to the user's timezone.
        - `/reminders title:My Reminder remind_date:2024-10-05 remind_time:17:00 repeat_interval:daily` shows the same example, but the reminder will repeat daily. The other options for repeat_interval are `weekly` and `monthly`.
- `/deletereminder [#]` will delete the reminder. To find the id of the reminder, use `/reminders`.
- `/help` was updated to display new timezone and reminder information.

## Upgrading Notes
The changes from v2.0.0 are minor. The reminders table was added to the MySQL database as well as the addition of the timezone field on the User table. 

To upgrade, start by creating the reminders table in your MySQL shell:
```sql
CREATE TABLE reminder (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    remind_at DATETIME NOT NULL,
    repeat_interval VARCHAR(50), -- e.g., 'daily', 'weekly', 'monthly'
    repeat_until DATETIME, -- The date until which the reminder should repeat, NULL means indefinitely
    repeat_count INT UNSIGNED, -- The number of times to repeat, NULL for indefinite or repeat until a specific date
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
```

and then add the timezone field to the user table:

```sql
ALTER TABLE user
ADD timezone VARCHAR(100) NOT NULL DEFAULT 'UTC';
```