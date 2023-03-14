import 'package:flutter/material.dart';

import '../theme/app_color.dart';

class buildButton extends StatelessWidget {
  buildButton(
      {super.key,
      required this.title,
      required this.icon,
      required this.onClicked});

  String title;
  IconData icon;
  VoidCallback onClicked;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8.0),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
            minimumSize: Size.fromHeight(56),
            primary: AppColor.primaryColor,
            onPrimary: Colors.white,
            textStyle: TextStyle(fontSize: 20)),
        onPressed: onClicked,
        child: Row(
          children: [
            Icon(
              icon,
              size: 28,
            ),
            const SizedBox(
              width: 16,
            ),
            Text(title)
          ],
        ),
      ),
    );
  }
}
