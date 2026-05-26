# Product Vision

## Purpose

This document defines the product idea, users, and long-term boundaries for CaloriesCounter.

## Product Idea

CaloriesCounter is a Telegram bot that helps users count calories and macros from simple food messages.

The intended experience is lightweight:

- the user sends food as text
- the bot replies with calories and macros
- the interaction stays faster and simpler than a full calorie-tracking app

## Core Value

The main product value is simplicity:

- no manual table lookup
- no heavy food-diary interface
- no need to open a traditional tracking app for every meal
- understandable nutrition feedback in chat

## Target Users

The product is intended for:

- users who want to lose weight
- users who want to maintain weight
- users who want to gain weight
- beginners who want a simpler alternative to traditional calorie trackers

## Product Principles

- Input should stay predictable and easy to explain.
- Early versions should favor reliability over magical interpretation.
- Output should be short and practical.
- Parsing failures should be explained clearly and politely.

## MVP Boundaries

Included in the MVP direction:

- Telegram bot interface
- food input as plain text
- calorie and macro calculation from a curated product database
- a simple `product + grams` contract

Not included in the MVP direction:

- image recognition
- broad recipe understanding
- automatic portion understanding such as `slice`, `spoon`, or `plate`
- diet coaching
- medical-grade personalization

## Growth Direction

The product is expected to grow in stages:

1. Basic calorie and macro counting from products
2. User profile data and base target calculation
3. Goal modes and target comparison

## Related Files

- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
- [Functional Requirements](F:\Python\CaloriesCounter\docs\functional-requirements.md)
- [Roadmap](F:\Python\CaloriesCounter\docs\roadmap.md)
