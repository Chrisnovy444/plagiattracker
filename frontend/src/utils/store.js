/**
 * Zustand State Management
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useUserStore = create(
  persist(
    (set) => ({
      user: null,
      email: null,

      setUser: (user) => set({ user, email: user?.email }),

      logout: () => set({ user: null, email: null }),

      updateAnalyses: (remaining) =>
        set((state) => ({
          user: state.user ? { ...state.user, analyses_remaining: remaining } : null,
        })),
    }),
    {
      name: 'plagiat-user-storage',
    }
  )
)

export const useDocumentStore = create((set) => ({
  currentDocument: null,
  uploadProgress: 0,

  setDocument: (doc) => set({ currentDocument: doc }),

  setProgress: (progress) => set({ uploadProgress: progress }),

  clearDocument: () => set({ currentDocument: null, uploadProgress: 0 }),
}))

export const useReportStore = create((set) => ({
  currentReport: null,
  loading: false,

  setReport: (report) => set({ currentReport: report, loading: false }),

  setLoading: (loading) => set({ loading }),

  clearReport: () => set({ currentReport: null, loading: false }),
}))
