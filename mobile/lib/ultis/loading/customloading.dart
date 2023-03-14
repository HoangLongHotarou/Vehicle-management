import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class CustomLoading{
  static loadingtext(BuildContext context, String? message) {
    showDialog(
      barrierDismissible: false,
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(builder: (context, setState) {
          return AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(20.0))),
              backgroundColor: Colors.white,
              content: Container(
                height: 100,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    SpinKitDualRing(
                      color: AppColor.primaryColor,
                      lineWidth: 8,
                      size: 48,
                    ),
                    Text('${message}',
                        style: Theme.of(context)
                            .textTheme
                            .headline6!
                            .copyWith(color: AppColor.primaryColor))
                  ],
                ),
              ));
        });
      }
    ); 
  }
  static void dismisloading(context){
      Navigator.of(context).pop();
  }
}