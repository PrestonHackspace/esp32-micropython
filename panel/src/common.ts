import { ActionResult } from 'hyperapp';
import { StatusState, StatusActions } from './modes/Status';
import { ScanState, ScanActions } from './modes/Scan';
import { SavedState, SavedActions } from './modes/Saved';

export interface ActionReturn<State, Actions> {
  (state: State, actions: Actions): ActionResult<State>;
}

export type AppViewMode = 'status' | 'scan' | 'saved';

export interface AppState {
  view: AppViewMode;

  status: StatusState;
  scan: ScanState;
  saved: SavedState;
}

export interface AppActions {
  setView(view: AppViewMode): ActionReturn<AppState, AppActions>;

  status: StatusActions;
  scan: ScanActions;
  saved: SavedActions;
}

export interface AppView {
  (state: AppState, action: AppActions): JSX.Element;
}

export interface StatefulView {
  (): (state: AppState, actions: AppActions) => JSX.Element;
}
