# Feature Specification: Greeting Banner

**Feature Branch**: `001-demo`

**Created**: 2026-10-11

**Status**: Draft

**Input**: User description: "Show a banner reading 'Welcome' on the home page."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See the banner (Priority: P1)

A visitor opens the home page and sees the banner.

**Acceptance Scenarios**:

1. **Given** the home page, **When** it loads, **Then** the banner reads exactly "Welcome".
2. **Given** a signed-in visitor and a signed-out visitor, **When** each loads the home page, **Then** both see the same banner in the same place.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The home page MUST show one banner whose text is exactly "Welcome" (English, no translation).
- **FR-002**: The banner MUST be a level-1 heading element, placed directly below the site header and navigation and above the page body.
- **FR-003**: The banner MUST be identical for every visitor, signed in or not, on every load.
- **FR-004**: The banner has no link, no close control, no animation and no styling beyond the site's default level-1 heading style.

## Success Criteria *(mandatory)*

- **SC-001**: The banner is visible with the text "Welcome" on 100% of home page loads in the acceptance test.

## Assumptions

- The site header, navigation and default heading style already exist and are not changed by this feature.
- Only the home page is in scope; no other page shows the banner.
- No performance, security, data or integration concerns apply to a static line of text.
