import 'package:flutter/material.dart';

import '../../../core/theme/app_color.dart';

class ConfirmButton extends StatelessWidget {
  ConfirmButton({super.key, required this.onClicked, required this.title});

  VoidCallback onClicked;
  String title;

  @override
  Widget build(BuildContext context) {
    return TextButton(
        onPressed: onClicked,
        child: Container(
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                color: AppColor.primaryColor),
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Text(title,
                style: Theme.of(context).textTheme.headlineSmall!.copyWith(
                      fontSize: 18,
                      color: AppColor.white,
                    ))));
  }
}
