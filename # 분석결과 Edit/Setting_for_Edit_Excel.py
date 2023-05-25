import pandas as pd
Filtering_threshold = {
    "iPhone 14 Pro": {
        # Preview Record
        "EIS OFF": {
            "threshold(patch size)": 50,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[300, 200, 600, 400],
                                           [150,   0, 300,   0],
                                           [500, 400, 300,   0],
                                           [150,   0, 800, 600],
                                           [500, 400, 800, 600]])
        },
        # Video Record
        "EIS ON": {
            "threshold(patch size)": 120,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[600,  400, 1200,  800],
                                           [300,    0,  600,    0],
                                           [1000, 800,  600,    0],
                                           [300,    0, 1600, 1200],
                                           [1000, 800, 1600, 1200]])
        }
    },
    "Galaxy S23 Ultra": {
        # Preview Record
        "EIS OFF": {
            "threshold(patch size)": 70,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[400, 200, 600, 500],
                                           [200,   0, 350,   0],
                                           [600, 400, 350,   0],
                                           [180,   0, 900, 720],
                                           [600, 400, 900, 750]])
        },
        # Video Record
        "EIS ON": {
            "threshold(patch size)": 120,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[650,  450, 1200,  800],
                                           [400,    0,  700,    0],
                                           [1000, 800,  700,    0],
                                           [300,    0, 1600, 1200],
                                           [1000, 800, 1600, 1200]])
        }
    },
    "Galaxy S22 Ultra": {
        # "EIS OFF": {
        #     "threshold(patch size)": 0,
        #     "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
        #                              data=[[300, 200, 600, 400],
        #                                    [150, 0, 300, 0],
        #                                    [500, 400, 300, 0],
        #                                    [150, 0, 800, 600],
        #                                    [500, 400, 800, 600]])
        # },
        "EIS ON": {
            "threshold(patch size)": 120,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[700, 400, 1100, 800],
                                           [400, 0, 700, 0],
                                           [1000, 700, 700, 0],
                                           [300, 0, 1600, 1200],
                                           [1000, 700, 1600, 1200]])
        }
    },
    "Galaxy S22 Ultra(UHD)": {
        # "EIS OFF": {
        #     "threshold(patch size)": 0,
        #     "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
        #                              data=[[300, 200, 600, 400],
        #                                    [150, 0, 300, 0],
        #                                    [500, 400, 300, 0],
        #                                    [150, 0, 800, 600],
        #                                    [500, 400, 800, 600]])
        # },
        "EIS ON": {
            "threshold(patch size)": 0,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[300, 200, 600, 400],
                                           [150, 0, 300, 0],
                                           [500, 400, 300, 0],
                                           [150, 0, 800, 600],
                                           [500, 400, 800, 600]])
        }
    },

    "Find X5 Pro": {
        # "EIS OFF": {
        #     "threshold(patch size)": 0,
        #     "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
        #                              data=[[300, 200, 600, 400],
        #                                    [150, 0, 300, 0],
        #                                    [500, 400, 300, 0],
        #                                    [150, 0, 800, 600],
        #                                    [500, 400, 800, 600]])
        # },
        "EIS ON": {
            "threshold(patch size)": 120,
            "ROI Info": pd.DataFrame(index=["C", "LT", "LB", "RT", "RB"], columns=["Ymax", "Ymin", "Xmax", "Xmin"],
                                     data=[[700, 400, 1100, 800],
                                           [400, 0, 700, 0],
                                           [1000, 700, 700, 0],
                                           [300, 0, 1600, 1200],
                                           [1000, 700, 1600, 1200]])
        }
    }
}