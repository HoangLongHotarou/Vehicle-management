import 'package:flutter/material.dart';

class Hello extends StatelessWidget {
  
  final String? username;
  
  const Hello({
    Key? key,
    required this.username
  }) ;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(top: 12, bottom: 4),
          child: Row(
            children: [
              Text(
                'Xin chào, ',
                style: Theme.of(context)
                    .textTheme
                    .headlineSmall!
                    .copyWith(color: Colors.grey),
              ),
              Text(
                username == null
                    ? 'khách!'
                    : username! + '!',
                style: Theme.of(context)
                    .textTheme
                    .headlineSmall!
                    .copyWith(color: Colors.grey),
              )
            ],
          ),
        ),
        Text(
          'Bạn muốn làm gì hôm nay?',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ],
    );
  }
}
