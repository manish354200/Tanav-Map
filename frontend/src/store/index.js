import { configureStore } from '@reduxjs/toolkit';

const initialState = {
  victims: [],
  alerts: [],
  interventions: [],
};

const appReducer = (state = initialState, action) => {
  switch (action.type) {
    default:
      return state;
  }
};

const store = configureStore({
  reducer: {
    app: appReducer,
  },
});

export default store;
