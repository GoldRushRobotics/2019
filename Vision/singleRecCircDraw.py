# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:24:26 2018

@author: Ziggy
"""

    if len(cntsB) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        for cB in cntsB:
        approx = cv2.approxPolyDP(cB, 0.01 * cv2.arcLength(cB, True), True)
        if len(approx) < 10:
            x, y, w, h = cv2.boundingRect(cB)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        elif len(approx) > 10:
            ((xB, yB), radiusB) = cv2.minEnclosingCircle(cB)
            mB = cv2.moments(cB)
            centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))

            # only proceed if the radius meets a minimum size
            if radiusB > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(xB), int(yB)), int(radiusB), (255, 0, 0), 2)
                cv2.circle(frame, centerB, 5, (0, 0, 0), -1)